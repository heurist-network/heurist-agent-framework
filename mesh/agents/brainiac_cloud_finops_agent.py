"""Auto-generated BRAINIAC Heurist Mesh agent for group `cloud-finops` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "cloud-finops__billing-csv-parse",
      "description": "Parse a billing CSV. Read brainiac-billing-v1 CSV or JSON charges. Required columns are date, service, cost, and currency. Native cloud-provider exports are rejected. Docs: https://www.brainiac.software/api/cloud-finops/billing-csv-parse",
      "parameters": {
        "type": "object",
        "properties": {
          "csv": {
            "type": "string",
            "minLength": 1,
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
                  "text/csv",
                  "text/plain"
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
          "rows": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "date": {
                  "type": "string",
                  "format": "date",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
                },
                "service": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "region": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "account": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "resourceId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "resourceType": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "usageQuantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "usageUnit": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "cost": {
                  "type": "number",
                  "minimum": -1000000000000,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "pattern": "^[A-Za-z]{3}$"
                },
                "tags": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "key": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 80
                      },
                      "value": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 200
                      }
                    },
                    "required": [
                      "key",
                      "value"
                    ],
                    "additionalProperties": false
                  }
                }
              },
              "required": [
                "date",
                "service",
                "cost",
                "currency"
              ],
              "additionalProperties": false
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
      "name": "cloud-finops__cost-anomaly-detect",
      "description": "Detect cost anomalies. Score daily totals with a sample z-score. A day is flagged when the absolute z-score is at least 3 and at least 8 days were supplied. Fewer days are not scored. Docs: https://www.brainiac.software/api/cloud-finops/cost-anomaly-detect",
      "parameters": {
        "type": "object",
        "properties": {
          "csv": {
            "type": "string",
            "minLength": 1,
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
                  "text/csv",
                  "text/plain"
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
          "rows": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "date": {
                  "type": "string",
                  "format": "date",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
                },
                "service": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "region": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "account": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "resourceId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "resourceType": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "usageQuantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "usageUnit": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "cost": {
                  "type": "number",
                  "minimum": -1000000000000,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "pattern": "^[A-Za-z]{3}$"
                },
                "tags": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "key": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 80
                      },
                      "value": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 200
                      }
                    },
                    "required": [
                      "key",
                      "value"
                    ],
                    "additionalProperties": false
                  }
                }
              },
              "required": [
                "date",
                "service",
                "cost",
                "currency"
              ],
              "additionalProperties": false
            }
          },
          "currency": {
            "type": "string",
            "pattern": "^[A-Za-z]{3}$"
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "cloud-finops__spend-breakdown",
      "description": "Break down cloud spend. Sum supplied charges by service, region, account, or a tag. When groupBy is omitted, charges are grouped by service. Currencies are not converted. Docs: https://www.brainiac.software/api/cloud-finops/spend-breakdown",
      "parameters": {
        "type": "object",
        "properties": {
          "csv": {
            "type": "string",
            "minLength": 1,
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
                  "text/csv",
                  "text/plain"
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
          "rows": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "date": {
                  "type": "string",
                  "format": "date",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
                },
                "service": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "region": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "account": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "resourceId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "resourceType": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "usageQuantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "usageUnit": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "cost": {
                  "type": "number",
                  "minimum": -1000000000000,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "pattern": "^[A-Za-z]{3}$"
                },
                "tags": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "key": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 80
                      },
                      "value": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 200
                      }
                    },
                    "required": [
                      "key",
                      "value"
                    ],
                    "additionalProperties": false
                  }
                }
              },
              "required": [
                "date",
                "service",
                "cost",
                "currency"
              ],
              "additionalProperties": false
            }
          },
          "groupBy": {
            "type": "string",
            "enum": [
              "service",
              "region",
              "account"
            ]
          },
          "tagKey": {
            "type": "string",
            "minLength": 1,
            "maxLength": 80
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "cloud-finops__idle-resource-detect",
      "description": "Detect idle compute. Mark compute idle only when daysObserved meets the supplied minimum and cpuPercent is below the supplied threshold. Missing CPU is not treated as idle. Docs: https://www.brainiac.software/api/cloud-finops/idle-resource-detect",
      "parameters": {
        "type": "object",
        "properties": {
          "resources": {
            "minItems": 1,
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "resourceId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "resourceType": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "daysObserved": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 3660
                },
                "cpuPercent": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "cost": {
                  "type": "number",
                  "minimum": -1000000000000,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "pattern": "^[A-Za-z]{3}$"
                }
              },
              "required": [
                "resourceId",
                "resourceType",
                "daysObserved"
              ],
              "additionalProperties": false
            }
          },
          "cpuThreshold": {
            "type": "number",
            "minimum": 0,
            "maximum": 100
          },
          "minimumDays": {
            "type": "integer",
            "minimum": 1,
            "maximum": 3660
          }
        },
        "required": [
          "resources"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "cloud-finops__unused-storage-detect",
      "description": "Detect unused storage. Mark a volume unused only when the supplied days meet minimumDays and the volume is unattached or usedGb is 0. Attachment alone is not usage. Docs: https://www.brainiac.software/api/cloud-finops/unused-storage-detect",
      "parameters": {
        "type": "object",
        "properties": {
          "volumes": {
            "minItems": 1,
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "resourceId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "storageGb": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "usedGb": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "attached": {
                  "type": "boolean"
                },
                "daysObserved": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 3660
                },
                "cost": {
                  "type": "number",
                  "minimum": -1000000000000,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "pattern": "^[A-Za-z]{3}$"
                }
              },
              "required": [
                "resourceId",
                "daysObserved"
              ],
              "additionalProperties": false
            }
          },
          "minimumDays": {
            "type": "integer",
            "minimum": 1,
            "maximum": 3660
          }
        },
        "required": [
          "volumes"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "cloud-finops__compute-cost-compare",
      "description": "Compare supplied compute prices. Multiply each supplied hourly price by the supplied hours. Options in different currencies are not converted, and no provider list price is added. Docs: https://www.brainiac.software/api/cloud-finops/compute-cost-compare",
      "parameters": {
        "type": "object",
        "properties": {
          "options": {
            "minItems": 2,
            "maxItems": 8,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "hourlyPrice": {
                  "type": "number",
                  "minimum": -1000000000000,
                  "maximum": 1000000000000
                },
                "hours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "currency": {
                  "type": "string",
                  "pattern": "^[A-Za-z]{3}$"
                }
              },
              "required": [
                "name",
                "hourlyPrice",
                "hours",
                "currency"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "options"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "cloud-finops__monthly-cost-forecast",
      "description": "Forecast monthly cloud cost. Fit a line through at least three supplied monthly totals, or multiply the average daily cost by the length of the next month when at least 14 days are supplied. Less history is not forecast. Docs: https://www.brainiac.software/api/cloud-finops/monthly-cost-forecast",
      "parameters": {
        "type": "object",
        "properties": {
          "csv": {
            "type": "string",
            "minLength": 1,
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
                  "text/csv",
                  "text/plain"
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
          "rows": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "date": {
                  "type": "string",
                  "format": "date",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
                },
                "service": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "region": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "account": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "resourceId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "resourceType": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "usageQuantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "usageUnit": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "cost": {
                  "type": "number",
                  "minimum": -1000000000000,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "pattern": "^[A-Za-z]{3}$"
                },
                "tags": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "key": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 80
                      },
                      "value": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 200
                      }
                    },
                    "required": [
                      "key",
                      "value"
                    ],
                    "additionalProperties": false
                  }
                }
              },
              "required": [
                "date",
                "service",
                "cost",
                "currency"
              ],
              "additionalProperties": false
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
      "name": "cloud-finops__budget-variance-analyze",
      "description": "Analyze budget variance. Subtract the supplied budget from the supplied charges inside the period. Missing days stay uncovered and are not filled with zero from another currency. Docs: https://www.brainiac.software/api/cloud-finops/budget-variance-analyze",
      "parameters": {
        "type": "object",
        "properties": {
          "csv": {
            "type": "string",
            "minLength": 1,
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
                  "text/csv",
                  "text/plain"
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
          "rows": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "date": {
                  "type": "string",
                  "format": "date",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
                },
                "service": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "region": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "account": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "resourceId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "resourceType": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "usageQuantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "usageUnit": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "cost": {
                  "type": "number",
                  "minimum": -1000000000000,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "pattern": "^[A-Za-z]{3}$"
                },
                "tags": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "key": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 80
                      },
                      "value": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 200
                      }
                    },
                    "required": [
                      "key",
                      "value"
                    ],
                    "additionalProperties": false
                  }
                }
              },
              "required": [
                "date",
                "service",
                "cost",
                "currency"
              ],
              "additionalProperties": false
            }
          },
          "budget": {
            "type": "object",
            "properties": {
              "amount": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000000000
              },
              "currency": {
                "type": "string",
                "pattern": "^[A-Za-z]{3}$"
              },
              "periodStart": {
                "type": "string",
                "format": "date",
                "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
              },
              "periodEnd": {
                "type": "string",
                "format": "date",
                "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
              }
            },
            "required": [
              "amount",
              "currency",
              "periodStart",
              "periodEnd"
            ],
            "additionalProperties": false
          }
        },
        "required": [
          "budget"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "cloud-finops__cost-allocation",
      "description": "Allocate cloud cost by tag. Group supplied charges by one tag key. Charges without that tag remain unallocated. Docs: https://www.brainiac.software/api/cloud-finops/cost-allocation",
      "parameters": {
        "type": "object",
        "properties": {
          "csv": {
            "type": "string",
            "minLength": 1,
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
                  "text/csv",
                  "text/plain"
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
          "rows": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "date": {
                  "type": "string",
                  "format": "date",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
                },
                "service": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "region": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "account": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "resourceId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "resourceType": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "usageQuantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "usageUnit": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "cost": {
                  "type": "number",
                  "minimum": -1000000000000,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "pattern": "^[A-Za-z]{3}$"
                },
                "tags": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "key": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 80
                      },
                      "value": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 200
                      }
                    },
                    "required": [
                      "key",
                      "value"
                    ],
                    "additionalProperties": false
                  }
                }
              },
              "required": [
                "date",
                "service",
                "cost",
                "currency"
              ],
              "additionalProperties": false
            }
          },
          "tagKey": {
            "type": "string",
            "minLength": 1,
            "maxLength": 80
          }
        },
        "required": [
          "tagKey"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "cloud-finops__cost-optimization-report",
      "description": "Report cloud cost evidence. Combine the supplied billing, usage, price, and budget checks. Recommendations repeat the evidence and the assumption. No account is connected and no resource is changed. Docs: https://www.brainiac.software/api/cloud-finops/cost-optimization-report",
      "parameters": {
        "type": "object",
        "properties": {
          "csv": {
            "type": "string",
            "minLength": 1,
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
                  "text/csv",
                  "text/plain"
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
          "rows": {
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "date": {
                  "type": "string",
                  "format": "date",
                  "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
                },
                "service": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "region": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "account": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "resourceId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "resourceType": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "usageQuantity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000000
                },
                "usageUnit": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "cost": {
                  "type": "number",
                  "minimum": -1000000000000,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "pattern": "^[A-Za-z]{3}$"
                },
                "tags": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "key": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 80
                      },
                      "value": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 200
                      }
                    },
                    "required": [
                      "key",
                      "value"
                    ],
                    "additionalProperties": false
                  }
                }
              },
              "required": [
                "date",
                "service",
                "cost",
                "currency"
              ],
              "additionalProperties": false
            }
          },
          "resources": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "resourceId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "resourceType": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "daysObserved": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 3660
                },
                "cpuPercent": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100
                },
                "cost": {
                  "type": "number",
                  "minimum": -1000000000000,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "pattern": "^[A-Za-z]{3}$"
                }
              },
              "required": [
                "resourceId",
                "resourceType",
                "daysObserved"
              ],
              "additionalProperties": false
            }
          },
          "volumes": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "resourceId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "storageGb": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "usedGb": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "attached": {
                  "type": "boolean"
                },
                "daysObserved": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 3660
                },
                "cost": {
                  "type": "number",
                  "minimum": -1000000000000,
                  "maximum": 1000000000000
                },
                "currency": {
                  "type": "string",
                  "pattern": "^[A-Za-z]{3}$"
                }
              },
              "required": [
                "resourceId",
                "daysObserved"
              ],
              "additionalProperties": false
            }
          },
          "cpuThreshold": {
            "type": "number",
            "minimum": 0,
            "maximum": 100
          },
          "minimumDays": {
            "type": "integer",
            "minimum": 1,
            "maximum": 3660
          },
          "options": {
            "minItems": 2,
            "maxItems": 8,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "hourlyPrice": {
                  "type": "number",
                  "minimum": -1000000000000,
                  "maximum": 1000000000000
                },
                "hours": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000
                },
                "currency": {
                  "type": "string",
                  "pattern": "^[A-Za-z]{3}$"
                }
              },
              "required": [
                "name",
                "hourlyPrice",
                "hours",
                "currency"
              ],
              "additionalProperties": false
            }
          },
          "budget": {
            "type": "object",
            "properties": {
              "amount": {
                "type": "number",
                "minimum": 0,
                "maximum": 1000000000000
              },
              "currency": {
                "type": "string",
                "pattern": "^[A-Za-z]{3}$"
              },
              "periodStart": {
                "type": "string",
                "format": "date",
                "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
              },
              "periodEnd": {
                "type": "string",
                "format": "date",
                "pattern": "^(?:(?:\\d\\d[2468][048]|\\d\\d[13579][26]|\\d\\d0[48]|[02468][048]00|[13579][26]00)-02-29|\\d{4}-(?:(?:0[13578]|1[02])-(?:0[1-9]|[12]\\d|3[01])|(?:0[469]|11)-(?:0[1-9]|[12]\\d|30)|(?:02)-(?:0[1-9]|1\\d|2[0-8])))$"
              }
            },
            "required": [
              "amount",
              "currency",
              "periodStart",
              "periodEnd"
            ],
            "additionalProperties": false
          },
          "tagKey": {
            "type": "string",
            "minLength": 1,
            "maxLength": 80
          },
          "groupBy": {
            "type": "string",
            "enum": [
              "service",
              "region",
              "account"
            ]
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "cloud-finops__billing-csv-parse": "0.03",
  "cloud-finops__cost-anomaly-detect": "0.04",
  "cloud-finops__spend-breakdown": "0.03",
  "cloud-finops__idle-resource-detect": "0.04",
  "cloud-finops__unused-storage-detect": "0.04",
  "cloud-finops__compute-cost-compare": "0.03",
  "cloud-finops__monthly-cost-forecast": "0.05",
  "cloud-finops__budget-variance-analyze": "0.03",
  "cloud-finops__cost-allocation": "0.04",
  "cloud-finops__cost-optimization-report": "0.12"
}
TOOL_ROUTES: Dict[str, str] = {
  "cloud-finops__billing-csv-parse": "cloud-finops/billing-csv-parse",
  "cloud-finops__cost-anomaly-detect": "cloud-finops/cost-anomaly-detect",
  "cloud-finops__spend-breakdown": "cloud-finops/spend-breakdown",
  "cloud-finops__idle-resource-detect": "cloud-finops/idle-resource-detect",
  "cloud-finops__unused-storage-detect": "cloud-finops/unused-storage-detect",
  "cloud-finops__compute-cost-compare": "cloud-finops/compute-cost-compare",
  "cloud-finops__monthly-cost-forecast": "cloud-finops/monthly-cost-forecast",
  "cloud-finops__budget-variance-analyze": "cloud-finops/budget-variance-analyze",
  "cloud-finops__cost-allocation": "cloud-finops/cost-allocation",
  "cloud-finops__cost-optimization-report": "cloud-finops/cost-optimization-report"
}


class BrainiacCloudFinopsAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — cloud-finops",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the cloud-finops catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "cloud-finops", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Parse a billing CSV"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.03",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the cloud-finops group. "
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
