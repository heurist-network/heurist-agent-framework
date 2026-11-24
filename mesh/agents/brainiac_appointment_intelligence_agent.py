"""Auto-generated BRAINIAC Heurist Mesh agent for group `appointment-intelligence` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "appointment-intelligence__data-normalize",
      "description": "Normalize appointment data. Copy supplied appointments, slots, and providers into a consistent inventory with status kinds and durations. Protected attributes are not accepted. No booking is modified. Docs: https://www.brainiac.software/api/appointment-intelligence/data-normalize",
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
          "appointments": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "clientId": {
                  "type": "string",
                  "maxLength": 80
                },
                "providerId": {
                  "type": "string",
                  "maxLength": 80
                },
                "service": {
                  "type": "string",
                  "maxLength": 160
                },
                "start": {
                  "type": "string",
                  "maxLength": 40
                },
                "end": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "bookedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "cancelledAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "reminderAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "channel": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "slots": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "providerId": {
                  "type": "string",
                  "maxLength": 80
                },
                "start": {
                  "type": "string",
                  "maxLength": 40
                },
                "end": {
                  "type": "string",
                  "maxLength": 40
                },
                "capacity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10000
                }
              },
              "additionalProperties": false
            }
          },
          "providers": {
            "maxItems": 40,
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
                "capacityMinutes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "minSample": {
            "type": "integer",
            "minimum": 1,
            "maximum": 100000
          },
          "gapMinutes": {
            "type": "integer",
            "minimum": 1,
            "maximum": 1440
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "appointment-intelligence__no-show-analyze",
      "description": "Analyze appointment no-shows. Calculate no-show rates by weekday, hour, and repeat client id from supplied history. Small samples are disclosed. Attendance is not predicted from protected attributes. Docs: https://www.brainiac.software/api/appointment-intelligence/no-show-analyze",
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
          "appointments": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "clientId": {
                  "type": "string",
                  "maxLength": 80
                },
                "providerId": {
                  "type": "string",
                  "maxLength": 80
                },
                "service": {
                  "type": "string",
                  "maxLength": 160
                },
                "start": {
                  "type": "string",
                  "maxLength": 40
                },
                "end": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "bookedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "cancelledAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "reminderAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "channel": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "slots": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "providerId": {
                  "type": "string",
                  "maxLength": 80
                },
                "start": {
                  "type": "string",
                  "maxLength": 40
                },
                "end": {
                  "type": "string",
                  "maxLength": 40
                },
                "capacity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10000
                }
              },
              "additionalProperties": false
            }
          },
          "providers": {
            "maxItems": 40,
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
                "capacityMinutes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "minSample": {
            "type": "integer",
            "minimum": 1,
            "maximum": 100000
          },
          "gapMinutes": {
            "type": "integer",
            "minimum": 1,
            "maximum": 1440
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "appointment-intelligence__cancellation-pattern-detect",
      "description": "Detect cancellation patterns. Find cancellations, short-notice lead times, and weekday patterns from supplied timestamps. Small samples are disclosed. Docs: https://www.brainiac.software/api/appointment-intelligence/cancellation-pattern-detect",
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
          "appointments": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "clientId": {
                  "type": "string",
                  "maxLength": 80
                },
                "providerId": {
                  "type": "string",
                  "maxLength": 80
                },
                "service": {
                  "type": "string",
                  "maxLength": 160
                },
                "start": {
                  "type": "string",
                  "maxLength": 40
                },
                "end": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "bookedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "cancelledAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "reminderAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "channel": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "slots": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "providerId": {
                  "type": "string",
                  "maxLength": 80
                },
                "start": {
                  "type": "string",
                  "maxLength": 40
                },
                "end": {
                  "type": "string",
                  "maxLength": 40
                },
                "capacity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10000
                }
              },
              "additionalProperties": false
            }
          },
          "providers": {
            "maxItems": 40,
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
                "capacityMinutes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "minSample": {
            "type": "integer",
            "minimum": 1,
            "maximum": 100000
          },
          "gapMinutes": {
            "type": "integer",
            "minimum": 1,
            "maximum": 1440
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "appointment-intelligence__capacity-analyze",
      "description": "Analyze appointment capacity. Compare booked appointment minutes with supplied provider capacity or slots. Overbooking is reported from those numbers only. Docs: https://www.brainiac.software/api/appointment-intelligence/capacity-analyze",
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
          "appointments": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "clientId": {
                  "type": "string",
                  "maxLength": 80
                },
                "providerId": {
                  "type": "string",
                  "maxLength": 80
                },
                "service": {
                  "type": "string",
                  "maxLength": 160
                },
                "start": {
                  "type": "string",
                  "maxLength": 40
                },
                "end": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "bookedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "cancelledAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "reminderAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "channel": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "slots": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "providerId": {
                  "type": "string",
                  "maxLength": 80
                },
                "start": {
                  "type": "string",
                  "maxLength": 40
                },
                "end": {
                  "type": "string",
                  "maxLength": 40
                },
                "capacity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10000
                }
              },
              "additionalProperties": false
            }
          },
          "providers": {
            "maxItems": 40,
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
                "capacityMinutes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "minSample": {
            "type": "integer",
            "minimum": 1,
            "maximum": 100000
          },
          "gapMinutes": {
            "type": "integer",
            "minimum": 1,
            "maximum": 1440
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "appointment-intelligence__schedule-utilization-calculate",
      "description": "Calculate schedule utilization. Calculate schedule and attendance utilization from supplied bookings and capacity. Recommendations describe observed fill levels only. Docs: https://www.brainiac.software/api/appointment-intelligence/schedule-utilization-calculate",
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
          "appointments": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "clientId": {
                  "type": "string",
                  "maxLength": 80
                },
                "providerId": {
                  "type": "string",
                  "maxLength": 80
                },
                "service": {
                  "type": "string",
                  "maxLength": 160
                },
                "start": {
                  "type": "string",
                  "maxLength": 40
                },
                "end": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "bookedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "cancelledAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "reminderAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "channel": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "slots": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "providerId": {
                  "type": "string",
                  "maxLength": 80
                },
                "start": {
                  "type": "string",
                  "maxLength": 40
                },
                "end": {
                  "type": "string",
                  "maxLength": 40
                },
                "capacity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10000
                }
              },
              "additionalProperties": false
            }
          },
          "providers": {
            "maxItems": 40,
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
                "capacityMinutes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "minSample": {
            "type": "integer",
            "minimum": 1,
            "maximum": 100000
          },
          "gapMinutes": {
            "type": "integer",
            "minimum": 1,
            "maximum": 1440
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "appointment-intelligence__booking-gap-detect",
      "description": "Detect booking gaps. Find gaps of at least the disclosed minute threshold between consecutive non-cancelled appointments for each provider. Docs: https://www.brainiac.software/api/appointment-intelligence/booking-gap-detect",
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
          "appointments": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "clientId": {
                  "type": "string",
                  "maxLength": 80
                },
                "providerId": {
                  "type": "string",
                  "maxLength": 80
                },
                "service": {
                  "type": "string",
                  "maxLength": 160
                },
                "start": {
                  "type": "string",
                  "maxLength": 40
                },
                "end": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "bookedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "cancelledAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "reminderAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "channel": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "slots": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "providerId": {
                  "type": "string",
                  "maxLength": 80
                },
                "start": {
                  "type": "string",
                  "maxLength": 40
                },
                "end": {
                  "type": "string",
                  "maxLength": 40
                },
                "capacity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10000
                }
              },
              "additionalProperties": false
            }
          },
          "providers": {
            "maxItems": 40,
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
                "capacityMinutes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "minSample": {
            "type": "integer",
            "minimum": 1,
            "maximum": 100000
          },
          "gapMinutes": {
            "type": "integer",
            "minimum": 1,
            "maximum": 1440
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "appointment-intelligence__reminder-timing-analyze",
      "description": "Analyze appointment reminder timing. Compare observed no-show rates across reminder lead-time windows from supplied reminder timestamps. No reminder is sent. Docs: https://www.brainiac.software/api/appointment-intelligence/reminder-timing-analyze",
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
          "appointments": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "clientId": {
                  "type": "string",
                  "maxLength": 80
                },
                "providerId": {
                  "type": "string",
                  "maxLength": 80
                },
                "service": {
                  "type": "string",
                  "maxLength": 160
                },
                "start": {
                  "type": "string",
                  "maxLength": 40
                },
                "end": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "bookedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "cancelledAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "reminderAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "channel": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "slots": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "providerId": {
                  "type": "string",
                  "maxLength": 80
                },
                "start": {
                  "type": "string",
                  "maxLength": 40
                },
                "end": {
                  "type": "string",
                  "maxLength": 40
                },
                "capacity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10000
                }
              },
              "additionalProperties": false
            }
          },
          "providers": {
            "maxItems": 40,
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
                "capacityMinutes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "minSample": {
            "type": "integer",
            "minimum": 1,
            "maximum": 100000
          },
          "gapMinutes": {
            "type": "integer",
            "minimum": 1,
            "maximum": 1440
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "appointment-intelligence__operations-report",
      "description": "Report appointment operations. Combine no-show patterns, cancellations, capacity, utilization, gaps, and reminder timing from supplied schedules. No reminder is sent and attendance is not predicted. Docs: https://www.brainiac.software/api/appointment-intelligence/operations-report",
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
          "appointments": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "clientId": {
                  "type": "string",
                  "maxLength": 80
                },
                "providerId": {
                  "type": "string",
                  "maxLength": 80
                },
                "service": {
                  "type": "string",
                  "maxLength": 160
                },
                "start": {
                  "type": "string",
                  "maxLength": 40
                },
                "end": {
                  "type": "string",
                  "maxLength": 40
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "bookedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "cancelledAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "reminderAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "channel": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "additionalProperties": false
            }
          },
          "slots": {
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "providerId": {
                  "type": "string",
                  "maxLength": 80
                },
                "start": {
                  "type": "string",
                  "maxLength": 40
                },
                "end": {
                  "type": "string",
                  "maxLength": 40
                },
                "capacity": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 10000
                }
              },
              "additionalProperties": false
            }
          },
          "providers": {
            "maxItems": 40,
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
                "capacityMinutes": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "minSample": {
            "type": "integer",
            "minimum": 1,
            "maximum": 100000
          },
          "gapMinutes": {
            "type": "integer",
            "minimum": 1,
            "maximum": 1440
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "appointment-intelligence__data-normalize": "0.04",
  "appointment-intelligence__no-show-analyze": "0.05",
  "appointment-intelligence__cancellation-pattern-detect": "0.04",
  "appointment-intelligence__capacity-analyze": "0.04",
  "appointment-intelligence__schedule-utilization-calculate": "0.05",
  "appointment-intelligence__booking-gap-detect": "0.04",
  "appointment-intelligence__reminder-timing-analyze": "0.05",
  "appointment-intelligence__operations-report": "0.12"
}
TOOL_ROUTES: Dict[str, str] = {
  "appointment-intelligence__data-normalize": "appointment-intelligence/data-normalize",
  "appointment-intelligence__no-show-analyze": "appointment-intelligence/no-show-analyze",
  "appointment-intelligence__cancellation-pattern-detect": "appointment-intelligence/cancellation-pattern-detect",
  "appointment-intelligence__capacity-analyze": "appointment-intelligence/capacity-analyze",
  "appointment-intelligence__schedule-utilization-calculate": "appointment-intelligence/schedule-utilization-calculate",
  "appointment-intelligence__booking-gap-detect": "appointment-intelligence/booking-gap-detect",
  "appointment-intelligence__reminder-timing-analyze": "appointment-intelligence/reminder-timing-analyze",
  "appointment-intelligence__operations-report": "appointment-intelligence/operations-report"
}


class BrainiacAppointmentIntelligenceAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — appointment-intelligence",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the appointment-intelligence catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "appointment-intelligence", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Normalize appointment data"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.04",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the appointment-intelligence group. "
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
