"""Auto-generated BRAINIAC Heurist Mesh agent for group `solar-design` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "solar-design__string-sizing",
      "description": "Size PV module strings for an inverter MPPT. Compute minimum and maximum modules per series string and maximum parallel strings per MPPT from module temperature coefficients, site temperatures and inverter DC limits. Docs: https://www.brainiac.software/api/solar-design/string-sizing",
      "parameters": {
        "type": "object",
        "properties": {
          "module": {
            "type": "object",
            "properties": {
              "voc": {
                "type": "number",
                "exclusiveMinimum": 0
              },
              "vmp": {
                "type": "number",
                "exclusiveMinimum": 0
              },
              "isc": {
                "type": "number",
                "exclusiveMinimum": 0
              },
              "imp": {
                "type": "number",
                "exclusiveMinimum": 0
              },
              "tempCoeffVoc": {
                "type": "number"
              },
              "tempCoeffVocUnit": {
                "type": "string",
                "enum": [
                  "V_per_C",
                  "fraction_per_C",
                  "percent_per_C",
                  "A_per_C"
                ]
              },
              "tempCoeffVmp": {
                "type": "number"
              },
              "tempCoeffVmpUnit": {
                "type": "string",
                "enum": [
                  "V_per_C",
                  "fraction_per_C",
                  "percent_per_C"
                ]
              },
              "tempCoeffIsc": {
                "type": "number"
              },
              "tempCoeffIscUnit": {
                "type": "string",
                "enum": [
                  "A_per_C",
                  "fraction_per_C",
                  "percent_per_C"
                ]
              },
              "bifacialGain": {
                "default": 0,
                "type": "number",
                "minimum": 0,
                "maximum": 0.5
              }
            },
            "required": [
              "voc",
              "vmp",
              "isc",
              "tempCoeffVoc",
              "tempCoeffVocUnit",
              "tempCoeffVmp",
              "tempCoeffVmpUnit",
              "tempCoeffIsc",
              "tempCoeffIscUnit"
            ],
            "additionalProperties": false
          },
          "site": {
            "type": "object",
            "properties": {
              "recordLowAmbient": {
                "type": "number"
              },
              "maxCellTemp": {
                "type": "number"
              }
            },
            "required": [
              "recordLowAmbient",
              "maxCellTemp"
            ],
            "additionalProperties": false
          },
          "inverter": {
            "type": "object",
            "properties": {
              "maxDcVoltage": {
                "type": "number",
                "exclusiveMinimum": 0
              },
              "mpptMin": {
                "type": "number",
                "exclusiveMinimum": 0
              },
              "mpptMax": {
                "type": "number",
                "exclusiveMinimum": 0
              },
              "maxInputCurrentPerMppt": {
                "type": "number",
                "exclusiveMinimum": 0
              },
              "maxIscPerMppt": {
                "anyOf": [
                  {
                    "type": "number",
                    "exclusiveMinimum": 0
                  },
                  {
                    "type": "null"
                  }
                ]
              }
            },
            "required": [
              "maxDcVoltage",
              "mpptMin",
              "mpptMax"
            ],
            "additionalProperties": false
          }
        },
        "required": [
          "module",
          "site",
          "inverter"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "solar-design__dc-ac-ratio-check",
      "description": "Check DC/AC ratio and inverter clipping. Compute the DC/AC ratio and optionally estimate AC energy and clipping from a caller DC power series with constant efficiency or a PVWatts inverter curve. Docs: https://www.brainiac.software/api/solar-design/dc-ac-ratio-check",
      "parameters": {
        "type": "object",
        "properties": {
          "dcNameplateKw": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "acRatingKw": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "inverterEfficiency": {
            "default": 0.96,
            "type": "number",
            "exclusiveMinimum": 0,
            "maximum": 1
          },
          "dcPowerSeriesKw": {
            "maxItems": 105408,
            "type": "array",
            "items": {
              "type": "number",
              "minimum": 0
            }
          },
          "intervalHours": {
            "default": 1,
            "type": "number",
            "exclusiveMinimum": 0
          },
          "ratioWarnAbove": {
            "default": 1.3,
            "type": "number",
            "exclusiveMinimum": 0
          },
          "useCecCurve": {
            "default": false,
            "type": "boolean"
          }
        },
        "required": [
          "dcNameplateKw",
          "acRatingKw"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "solar-design__poa-irradiance-transpose",
      "description": "Transpose GHI/DNI/DHI to plane-of-array irradiance. Compute plane-of-array irradiance with isotropic, Hay-Davies or Perez sky models and NREL SPA solar geometry from caller irradiance records. Docs: https://www.brainiac.software/api/solar-design/poa-irradiance-transpose",
      "parameters": {
        "type": "object",
        "properties": {
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
          "elevation": {
            "default": 0,
            "type": "number"
          },
          "tilt": {
            "type": "number",
            "minimum": 0,
            "maximum": 90
          },
          "azimuth": {
            "type": "number",
            "minimum": 0,
            "maximum": 360
          },
          "albedo": {
            "default": 0.2,
            "type": "number",
            "minimum": 0,
            "maximum": 1
          },
          "model": {
            "default": "perez",
            "type": "string",
            "enum": [
              "isotropic",
              "haydavies",
              "perez"
            ]
          },
          "records": {
            "minItems": 1,
            "maxItems": 105408,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "time": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 64
                },
                "ghi": {
                  "type": "number",
                  "minimum": 0
                },
                "dni": {
                  "type": "number",
                  "minimum": 0
                },
                "dhi": {
                  "type": "number",
                  "minimum": 0
                }
              },
              "required": [
                "time",
                "ghi",
                "dni",
                "dhi"
              ],
              "additionalProperties": false
            }
          },
          "pressurePa": {
            "default": 101325,
            "type": "number",
            "exclusiveMinimum": 0
          },
          "temperatureC": {
            "default": 12,
            "type": "number"
          },
          "deltaT": {
            "default": 67,
            "type": "number"
          }
        },
        "required": [
          "latitude",
          "longitude",
          "tilt",
          "azimuth",
          "records"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "solar-design__energy-yield-estimate",
      "description": "Estimate AC energy with PVWatts v5. Estimate AC energy from caller POA irradiance and temperatures using the PVWatts v5 DC and inverter models with a transparent loss stack. Docs: https://www.brainiac.software/api/solar-design/energy-yield-estimate",
      "parameters": {
        "type": "object",
        "properties": {
          "dcNameplateW": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "gammaPdc": {
            "type": "number"
          },
          "acRatingW": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "inverterNominalEfficiency": {
            "default": 0.96,
            "type": "number",
            "exclusiveMinimum": 0,
            "maximum": 1
          },
          "lossesPercent": {
            "default": 14.08,
            "type": "number",
            "minimum": 0,
            "maximum": 100
          },
          "temperatureModel": {
            "type": "object",
            "properties": {
              "type": {
                "type": "string",
                "const": "pvsyst"
              },
              "uc": {
                "default": 29,
                "type": "number",
                "exclusiveMinimum": 0
              },
              "uv": {
                "default": 0,
                "type": "number",
                "minimum": 0
              },
              "alphaAbsorption": {
                "default": 0.9,
                "type": "number",
                "exclusiveMinimum": 0,
                "maximum": 1
              },
              "moduleEfficiency": {
                "default": 0.1,
                "type": "number",
                "exclusiveMinimum": 0,
                "maximum": 1
              }
            },
            "required": [
              "type"
            ],
            "additionalProperties": false
          },
          "records": {
            "minItems": 1,
            "maxItems": 105408,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "time": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 64
                },
                "poa": {
                  "type": "number",
                  "minimum": 0
                },
                "ambientTemp": {
                  "type": "number"
                },
                "windSpeed": {
                  "default": 1,
                  "type": "number",
                  "minimum": 0
                },
                "cellTemp": {
                  "type": "number"
                }
              },
              "required": [
                "time",
                "poa"
              ],
              "additionalProperties": false
            }
          },
          "monthly": {
            "minItems": 12,
            "maxItems": 12,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "poaKwhPerM2": {
                  "type": "number",
                  "minimum": 0
                },
                "avgAmbientTemp": {
                  "type": "number"
                }
              },
              "required": [
                "poaKwhPerM2",
                "avgAmbientTemp"
              ],
              "additionalProperties": false
            }
          },
          "intervalHours": {
            "default": 1,
            "type": "number",
            "exclusiveMinimum": 0
          }
        },
        "required": [
          "dcNameplateW",
          "gammaPdc",
          "acRatingW"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "solar-design__row-spacing",
      "description": "Compute inter-row spacing and GCR. Compute row height, shadow gap, row pitch and ground coverage ratio that avoid row-to-row shading at a design sun position. Docs: https://www.brainiac.software/api/solar-design/row-spacing",
      "parameters": {
        "type": "object",
        "properties": {
          "moduleSlopeLength": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "tilt": {
            "type": "number",
            "minimum": 0,
            "maximum": 90
          },
          "arrayAzimuth": {
            "default": 180,
            "type": "number",
            "minimum": 0,
            "maximum": 360
          },
          "sun": {
            "type": "object",
            "properties": {
              "elevation": {
                "type": "number"
              },
              "azimuth": {
                "type": "number",
                "minimum": 0,
                "maximum": 360
              }
            },
            "required": [
              "elevation",
              "azimuth"
            ],
            "additionalProperties": false
          },
          "designTimes": {
            "maxItems": 48,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 64
            }
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
          "elevation": {
            "default": 0,
            "type": "number"
          },
          "groundSlope": {
            "default": 0,
            "type": "number"
          }
        },
        "required": [
          "moduleSlopeLength",
          "tilt"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "solar-design__horizon-shading-loss",
      "description": "Estimate far-field horizon shading losses. Estimate beam and isotropic sky-diffuse losses caused by a caller far-field horizon profile against sun positions and beam POA. Docs: https://www.brainiac.software/api/solar-design/horizon-shading-loss",
      "parameters": {
        "type": "object",
        "properties": {
          "horizon": {
            "minItems": 4,
            "maxItems": 360,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "azimuth": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 360
                },
                "elevation": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 90
                }
              },
              "required": [
                "azimuth",
                "elevation"
              ],
              "additionalProperties": false
            }
          },
          "records": {
            "minItems": 1,
            "maxItems": 105408,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "sunElevation": {
                  "type": "number"
                },
                "sunAzimuth": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 360
                },
                "beamPoa": {
                  "type": "number",
                  "minimum": 0
                }
              },
              "required": [
                "sunElevation",
                "sunAzimuth",
                "beamPoa"
              ],
              "additionalProperties": false
            }
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
          "elevation": {
            "default": 0,
            "type": "number"
          },
          "times": {
            "maxItems": 105408,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 64
            }
          },
          "beamPoa": {
            "maxItems": 105408,
            "type": "array",
            "items": {
              "type": "number",
              "minimum": 0
            }
          }
        },
        "required": [
          "horizon"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "solar-design__system-loss-stack",
      "description": "Combine PVWatts system loss percentages. Combine individual loss percentages into a total system loss using PVWatts multiplicative derating, with optional defaults for missing categories. Docs: https://www.brainiac.software/api/solar-design/system-loss-stack",
      "parameters": {
        "type": "object",
        "properties": {
          "losses": {
            "default": {},
            "type": "object",
            "propertyNames": {
              "type": "string",
              "minLength": 1,
              "maxLength": 64
            },
            "additionalProperties": {
              "type": "number",
              "minimum": 0,
              "maximum": 100
            }
          },
          "useDefaultsForMissing": {
            "default": true,
            "type": "boolean"
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "solar-design__battery-backup-sizing",
      "description": "Size battery backup energy and inverter power. Size battery energy and inverter continuous/surge power needed to back up critical loads for a target autonomy with DoD and efficiency derates. Docs: https://www.brainiac.software/api/solar-design/battery-backup-sizing",
      "parameters": {
        "type": "object",
        "properties": {
          "loads": {
            "minItems": 1,
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 128
                },
                "powerKw": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "hoursPerDay": {
                  "type": "number",
                  "exclusiveMinimum": 0,
                  "maximum": 24
                },
                "surgeKw": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "dutyFactor": {
                  "default": 1,
                  "type": "number",
                  "exclusiveMinimum": 0,
                  "maximum": 1
                }
              },
              "required": [
                "name",
                "powerKw",
                "hoursPerDay"
              ],
              "additionalProperties": false
            }
          },
          "autonomyHours": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "depthOfDischarge": {
            "type": "number",
            "exclusiveMinimum": 0,
            "maximum": 1
          },
          "dischargeEfficiency": {
            "type": "number",
            "exclusiveMinimum": 0,
            "maximum": 1
          },
          "temperatureDerate": {
            "default": 1,
            "type": "number",
            "exclusiveMinimum": 0,
            "maximum": 1
          },
          "inverterMargin": {
            "default": 1.25,
            "type": "number",
            "exclusiveMinimum": 0
          },
          "pvRechargeKwhPerDay": {
            "default": 0,
            "type": "number",
            "minimum": 0
          },
          "simultaneousStart": {
            "default": false,
            "type": "boolean"
          }
        },
        "required": [
          "loads",
          "autonomyHours",
          "depthOfDischarge",
          "dischargeEfficiency"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "solar-design__tariff-savings",
      "description": "Estimate bill savings under a TOU tariff. Compute bill savings from caller interval generation and load under a time-of-use tariff with export credit, net metering or no export value. Docs: https://www.brainiac.software/api/solar-design/tariff-savings",
      "parameters": {
        "type": "object",
        "properties": {
          "intervalHours": {
            "default": 1,
            "type": "number",
            "exclusiveMinimum": 0
          },
          "loadKwh": {
            "minItems": 1,
            "maxItems": 105408,
            "type": "array",
            "items": {
              "type": "number",
              "minimum": 0
            }
          },
          "generationKwh": {
            "minItems": 1,
            "maxItems": 105408,
            "type": "array",
            "items": {
              "type": "number",
              "minimum": 0
            }
          },
          "importPrice": {
            "minItems": 1,
            "maxItems": 105408,
            "type": "array",
            "items": {
              "type": "number"
            }
          },
          "exportMode": {
            "default": "export_rate",
            "type": "string",
            "enum": [
              "export_rate",
              "net_metering_kwh",
              "none"
            ]
          },
          "exportPrice": {
            "default": 0,
            "type": "number",
            "minimum": 0
          },
          "fixedCharges": {
            "default": 0,
            "type": "number",
            "minimum": 0
          },
          "demandCharge": {
            "anyOf": [
              {
                "type": "object",
                "properties": {
                  "pricePerKw": {
                    "type": "number",
                    "minimum": 0
                  },
                  "window": {
                    "minItems": 1,
                    "maxItems": 105408,
                    "type": "array",
                    "items": {
                      "type": "integer",
                      "minimum": 0,
                      "maximum": 9007199254740991
                    }
                  }
                },
                "required": [
                  "pricePerKw"
                ],
                "additionalProperties": false
              },
              {
                "type": "null"
              }
            ]
          },
          "billingPeriods": {
            "type": "array",
            "items": {
              "type": "integer",
              "minimum": 0,
              "maximum": 9007199254740991
            }
          }
        },
        "required": [
          "loadKwh",
          "generationKwh",
          "importPrice"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "solar-design__financial-payback",
      "description": "Compute PV payback, NPV, IRR and LCOE. Compute simple payback, NPV, IRR and LCOE from capex, incentives, year-1 energy, degradation, O&M and price escalation. Docs: https://www.brainiac.software/api/solar-design/financial-payback",
      "parameters": {
        "type": "object",
        "properties": {
          "capex": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "upfrontIncentives": {
            "default": 0,
            "type": "number",
            "minimum": 0
          },
          "year1EnergyKwh": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "degradation": {
            "default": 0.005,
            "type": "number",
            "minimum": -0.5,
            "maximum": 1
          },
          "energyValuePerKwh": {
            "type": "number"
          },
          "energyEscalation": {
            "default": 0.02,
            "type": "number",
            "minimum": -0.5,
            "maximum": 1
          },
          "omPerYear": {
            "default": 0,
            "type": "number",
            "minimum": 0
          },
          "omEscalation": {
            "default": 0.02,
            "type": "number",
            "minimum": -0.5,
            "maximum": 1
          },
          "years": {
            "type": "integer",
            "minimum": 1,
            "maximum": 50
          },
          "discountRate": {
            "type": "number",
            "minimum": -0.5,
            "maximum": 1
          }
        },
        "required": [
          "capex",
          "year1EnergyKwh",
          "energyValuePerKwh",
          "years",
          "discountRate"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "solar-design__module-layout-fit",
      "description": "Fit modules onto a roof polygon. Maximise the number of modules on a roof-face polygon with caller setbacks, orientation, gaps and obstruction polygons. Docs: https://www.brainiac.software/api/solar-design/module-layout-fit",
      "parameters": {
        "type": "object",
        "properties": {
          "roof": {
            "minItems": 3,
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "array",
              "prefixItems": [
                {
                  "type": "number"
                },
                {
                  "type": "number"
                }
              ],
              "items": false,
              "minItems": 2,
              "maxItems": 2
            }
          },
          "setback": {
            "type": "number",
            "minimum": 0
          },
          "module": {
            "type": "object",
            "properties": {
              "width": {
                "type": "number",
                "exclusiveMinimum": 0
              },
              "height": {
                "type": "number",
                "exclusiveMinimum": 0
              }
            },
            "required": [
              "width",
              "height"
            ],
            "additionalProperties": false
          },
          "gap": {
            "default": 0.02,
            "type": "number",
            "minimum": 0
          },
          "orientations": {
            "default": [
              "portrait",
              "landscape"
            ],
            "minItems": 1,
            "maxItems": 2,
            "type": "array",
            "items": {
              "type": "string",
              "enum": [
                "portrait",
                "landscape"
              ]
            }
          },
          "obstructions": {
            "default": [],
            "maxItems": 50,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "polygon": {
                  "minItems": 3,
                  "maxItems": 100,
                  "type": "array",
                  "items": {
                    "type": "array",
                    "prefixItems": [
                      {
                        "type": "number"
                      },
                      {
                        "type": "number"
                      }
                    ],
                    "items": false,
                    "minItems": 2,
                    "maxItems": 2
                  }
                },
                "setback": {
                  "default": 0,
                  "type": "number",
                  "minimum": 0
                }
              },
              "required": [
                "polygon"
              ],
              "additionalProperties": false
            }
          },
          "gridOffsets": {
            "default": 10,
            "type": "integer",
            "minimum": 1,
            "maximum": 25
          }
        },
        "required": [
          "roof",
          "setback",
          "module"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "solar-design__nec-690-current",
      "description": "Compute NEC 690.8 PV circuit current. Compute PV circuit maximum current and minimum conductor ampacity using NEC 690.8 125% factors for the selected code edition. Docs: https://www.brainiac.software/api/solar-design/nec-690-current",
      "parameters": {
        "type": "object",
        "properties": {
          "edition": {
            "default": "2023",
            "type": "string",
            "enum": [
              "2017",
              "2020",
              "2023"
            ]
          },
          "moduleIsc": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "parallelStrings": {
            "default": 1,
            "type": "integer",
            "exclusiveMinimum": 0,
            "maximum": 9007199254740991
          },
          "continuousFactor": {
            "default": 1.25,
            "type": "number",
            "exclusiveMinimum": 0
          }
        },
        "required": [
          "moduleIsc"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "solar-design__module-spec-compare",
      "description": "Compare module datasheet metrics. Normalise and compare module datasheet values for efficiency, W/m², temperature-adjusted power, price per watt and warranty retention. Docs: https://www.brainiac.software/api/solar-design/module-spec-compare",
      "parameters": {
        "type": "object",
        "properties": {
          "modules": {
            "minItems": 2,
            "maxItems": 50,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 128
                },
                "pmax": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "width": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "height": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "tempCoeffPmax": {
                  "type": "number"
                },
                "price": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "warrantyYear25Retention": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                },
                "noct": {
                  "type": "number"
                },
                "pmaxNoct": {
                  "type": "number"
                }
              },
              "required": [
                "name",
                "pmax"
              ],
              "additionalProperties": false
            }
          },
          "referenceCellTemp": {
            "default": 45,
            "type": "number"
          }
        },
        "required": [
          "modules"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "solar-design__pan-ond-parse",
      "description": "Parse PVsyst PAN or OND text files. Parse PVsyst PAN (module) and OND (inverter) text files into nested raw JSON and a normalised datasheet object. Docs: https://www.brainiac.software/api/solar-design/pan-ond-parse",
      "parameters": {
        "type": "object",
        "properties": {
          "fileType": {
            "type": "string",
            "enum": [
              "pan",
              "ond"
            ]
          },
          "content": {
            "type": "string",
            "minLength": 1,
            "maxLength": 524288
          }
        },
        "required": [
          "fileType",
          "content"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "solar-design__string-sizing": "0.03",
  "solar-design__dc-ac-ratio-check": "0.03",
  "solar-design__poa-irradiance-transpose": "0.04",
  "solar-design__energy-yield-estimate": "0.04",
  "solar-design__row-spacing": "0.02",
  "solar-design__horizon-shading-loss": "0.03",
  "solar-design__system-loss-stack": "0.01",
  "solar-design__battery-backup-sizing": "0.03",
  "solar-design__tariff-savings": "0.03",
  "solar-design__financial-payback": "0.03",
  "solar-design__module-layout-fit": "0.04",
  "solar-design__nec-690-current": "0.02",
  "solar-design__module-spec-compare": "0.02",
  "solar-design__pan-ond-parse": "0.02"
}
TOOL_ROUTES: Dict[str, str] = {
  "solar-design__string-sizing": "solar-design/string-sizing",
  "solar-design__dc-ac-ratio-check": "solar-design/dc-ac-ratio-check",
  "solar-design__poa-irradiance-transpose": "solar-design/poa-irradiance-transpose",
  "solar-design__energy-yield-estimate": "solar-design/energy-yield-estimate",
  "solar-design__row-spacing": "solar-design/row-spacing",
  "solar-design__horizon-shading-loss": "solar-design/horizon-shading-loss",
  "solar-design__system-loss-stack": "solar-design/system-loss-stack",
  "solar-design__battery-backup-sizing": "solar-design/battery-backup-sizing",
  "solar-design__tariff-savings": "solar-design/tariff-savings",
  "solar-design__financial-payback": "solar-design/financial-payback",
  "solar-design__module-layout-fit": "solar-design/module-layout-fit",
  "solar-design__nec-690-current": "solar-design/nec-690-current",
  "solar-design__module-spec-compare": "solar-design/module-spec-compare",
  "solar-design__pan-ond-parse": "solar-design/pan-ond-parse"
}


class BrainiacSolarDesignAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — solar-design",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the solar-design catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "solar-design", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Size PV module strings for an inverter MPPT"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.01",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the solar-design group. "
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
