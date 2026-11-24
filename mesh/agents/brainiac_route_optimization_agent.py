"""Auto-generated BRAINIAC Heurist Mesh agent for group `route-optimization` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "route-optimization__distance-matrix",
      "description": "Great-circle distance and duration matrix. Build a haversine distance and estimated duration matrix from caller coordinates with optional circuity and speed. Docs: https://www.brainiac.software/api/route-optimization/distance-matrix",
      "parameters": {
        "type": "object",
        "properties": {
          "locations": {
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
                "lat": {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90
                },
                "lon": {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180
                }
              },
              "required": [
                "id",
                "lat",
                "lon"
              ],
              "additionalProperties": false
            }
          },
          "circuity": {
            "type": "number",
            "minimum": 1,
            "maximum": 3
          },
          "speedKph": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "speedMps": {
            "type": "number",
            "exclusiveMinimum": 0
          }
        },
        "required": [
          "locations"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "route-optimization__tsp-optimize",
      "description": "Travelling salesman route order. Find a best visiting order for one vehicle (closed tour or open path) with fixed start and optional fixed end using Held-Karp or local search. Docs: https://www.brainiac.software/api/route-optimization/tsp-optimize",
      "parameters": {
        "type": "object",
        "properties": {
          "locations": {
            "minItems": 2,
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
                "x": {
                  "type": "number"
                },
                "y": {
                  "type": "number"
                },
                "lat": {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90
                },
                "lon": {
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
          "matrix": {
            "type": "object",
            "properties": {
              "distances": {
                "minItems": 1,
                "maxItems": 2000,
                "type": "array",
                "items": {
                  "type": "array",
                  "items": {
                    "type": "number"
                  }
                }
              },
              "durations": {
                "minItems": 1,
                "maxItems": 2000,
                "type": "array",
                "items": {
                  "type": "array",
                  "items": {
                    "type": "number"
                  }
                }
              }
            },
            "required": [
              "distances"
            ],
            "additionalProperties": false
          },
          "matrixFromPoints": {
            "type": "string",
            "enum": [
              "euclidean",
              "haversine"
            ]
          },
          "circuity": {
            "type": "number",
            "minimum": 1,
            "maximum": 3
          },
          "speedMps": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "speed": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "start": {
            "type": "string",
            "minLength": 1,
            "maxLength": 120
          },
          "end": {
            "anyOf": [
              {
                "type": "string",
                "minLength": 1,
                "maxLength": 120
              },
              {
                "type": "null"
              }
            ]
          },
          "objective": {
            "type": "string",
            "enum": [
              "distance",
              "duration"
            ]
          },
          "timeLimitMs": {
            "type": "integer",
            "minimum": 1,
            "maximum": 25000
          }
        },
        "required": [
          "locations",
          "start"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "route-optimization__vrp-capacitated",
      "description": "Capacitated vehicle routing. Assign stops to vehicles under capacity (and optional duration) limits, returning routes with loads and distances. Docs: https://www.brainiac.software/api/route-optimization/vrp-capacitated",
      "parameters": {
        "type": "object",
        "properties": {
          "depot": {
            "type": "object",
            "properties": {
              "id": {
                "type": "string",
                "minLength": 1,
                "maxLength": 120
              },
              "x": {
                "type": "number"
              },
              "y": {
                "type": "number"
              },
              "lat": {
                "type": "number",
                "minimum": -90,
                "maximum": 90
              },
              "lon": {
                "type": "number",
                "minimum": -180,
                "maximum": 180
              }
            },
            "required": [
              "id"
            ],
            "additionalProperties": false
          },
          "stops": {
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
                "x": {
                  "type": "number"
                },
                "y": {
                  "type": "number"
                },
                "lat": {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90
                },
                "lon": {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180
                },
                "demand": {
                  "anyOf": [
                    {
                      "type": "number",
                      "minimum": 0
                    },
                    {
                      "minItems": 1,
                      "maxItems": 8,
                      "type": "array",
                      "items": {
                        "type": "number",
                        "minimum": 0
                      }
                    }
                  ]
                }
              },
              "required": [
                "id",
                "demand"
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
                "capacity": {
                  "anyOf": [
                    {
                      "type": "number",
                      "minimum": 0
                    },
                    {
                      "minItems": 1,
                      "maxItems": 8,
                      "type": "array",
                      "items": {
                        "type": "number",
                        "minimum": 0
                      }
                    }
                  ]
                },
                "start": {
                  "type": "object",
                  "properties": {
                    "id": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 120
                    },
                    "x": {
                      "type": "number"
                    },
                    "y": {
                      "type": "number"
                    },
                    "lat": {
                      "type": "number",
                      "minimum": -90,
                      "maximum": 90
                    },
                    "lon": {
                      "type": "number",
                      "minimum": -180,
                      "maximum": 180
                    }
                  },
                  "required": [
                    "id"
                  ],
                  "additionalProperties": false
                },
                "end": {
                  "type": "object",
                  "properties": {
                    "id": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 120
                    },
                    "x": {
                      "type": "number"
                    },
                    "y": {
                      "type": "number"
                    },
                    "lat": {
                      "type": "number",
                      "minimum": -90,
                      "maximum": 90
                    },
                    "lon": {
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
              "required": [
                "id",
                "capacity"
              ],
              "additionalProperties": false
            }
          },
          "matrix": {
            "type": "object",
            "properties": {
              "distances": {
                "minItems": 1,
                "maxItems": 2000,
                "type": "array",
                "items": {
                  "type": "array",
                  "items": {
                    "type": "number"
                  }
                }
              },
              "durations": {
                "minItems": 1,
                "maxItems": 2000,
                "type": "array",
                "items": {
                  "type": "array",
                  "items": {
                    "type": "number"
                  }
                }
              }
            },
            "required": [
              "distances"
            ],
            "additionalProperties": false
          },
          "matrixFromPoints": {
            "type": "string",
            "enum": [
              "euclidean",
              "haversine"
            ]
          },
          "circuity": {
            "type": "number",
            "minimum": 1,
            "maximum": 3
          },
          "speedMps": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "speed": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "maxRouteDuration": {
            "anyOf": [
              {
                "type": "number",
                "minimum": 0
              },
              {
                "type": "null"
              }
            ]
          },
          "minimise": {
            "type": "string",
            "enum": [
              "distance",
              "duration"
            ]
          },
          "timeLimitMs": {
            "type": "integer",
            "minimum": 1,
            "maximum": 25000
          }
        },
        "required": [
          "depot",
          "stops",
          "vehicles"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "route-optimization__vrp-time-windows",
      "description": "Vehicle routing with time windows. Route stops under customer time windows, service times, driver shifts and breaks with forward time propagation. Docs: https://www.brainiac.software/api/route-optimization/vrp-time-windows",
      "parameters": {
        "type": "object",
        "properties": {
          "depot": {
            "type": "object",
            "properties": {
              "id": {
                "type": "string",
                "minLength": 1,
                "maxLength": 120
              },
              "x": {
                "type": "number"
              },
              "y": {
                "type": "number"
              },
              "lat": {
                "type": "number",
                "minimum": -90,
                "maximum": 90
              },
              "lon": {
                "type": "number",
                "minimum": -180,
                "maximum": 180
              },
              "window": {
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
            "required": [
              "id"
            ],
            "additionalProperties": false
          },
          "stops": {
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
                "x": {
                  "type": "number"
                },
                "y": {
                  "type": "number"
                },
                "lat": {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90
                },
                "lon": {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180
                },
                "window": {
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
                },
                "service": {
                  "type": "number",
                  "minimum": 0
                },
                "demand": {
                  "anyOf": [
                    {
                      "type": "number",
                      "minimum": 0
                    },
                    {
                      "minItems": 1,
                      "maxItems": 8,
                      "type": "array",
                      "items": {
                        "type": "number",
                        "minimum": 0
                      }
                    }
                  ]
                }
              },
              "required": [
                "id",
                "window"
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
                "shift": {
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
                },
                "breaks": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "window": {
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
                      },
                      "duration": {
                        "type": "number",
                        "minimum": 0
                      }
                    },
                    "required": [
                      "window",
                      "duration"
                    ],
                    "additionalProperties": false
                  }
                },
                "capacity": {
                  "anyOf": [
                    {
                      "type": "number",
                      "minimum": 0
                    },
                    {
                      "minItems": 1,
                      "maxItems": 8,
                      "type": "array",
                      "items": {
                        "type": "number",
                        "minimum": 0
                      }
                    }
                  ]
                }
              },
              "required": [
                "id",
                "shift"
              ],
              "additionalProperties": false
            }
          },
          "matrix": {
            "type": "object",
            "properties": {
              "distances": {
                "minItems": 1,
                "maxItems": 2000,
                "type": "array",
                "items": {
                  "type": "array",
                  "items": {
                    "type": "number"
                  }
                }
              },
              "durations": {
                "minItems": 1,
                "maxItems": 2000,
                "type": "array",
                "items": {
                  "type": "array",
                  "items": {
                    "type": "number"
                  }
                }
              }
            },
            "required": [
              "distances"
            ],
            "additionalProperties": false
          },
          "matrixFromPoints": {
            "type": "string",
            "enum": [
              "euclidean",
              "haversine"
            ]
          },
          "circuity": {
            "type": "number",
            "minimum": 1,
            "maximum": 3
          },
          "speed": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "speedMps": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "minimise": {
            "type": "string",
            "enum": [
              "distance",
              "completion_time",
              "vehicles"
            ]
          },
          "timeLimitMs": {
            "type": "integer",
            "minimum": 1,
            "maximum": 25000
          }
        },
        "required": [
          "depot",
          "stops",
          "vehicles"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "route-optimization__pickup-delivery",
      "description": "Pickup and delivery routing. Route paired pickup-and-delivery requests with precedence, same-vehicle and capacity constraints. Docs: https://www.brainiac.software/api/route-optimization/pickup-delivery",
      "parameters": {
        "type": "object",
        "properties": {
          "depot": {
            "type": "object",
            "properties": {
              "id": {
                "type": "string",
                "minLength": 1,
                "maxLength": 120
              },
              "x": {
                "type": "number"
              },
              "y": {
                "type": "number"
              },
              "lat": {
                "type": "number",
                "minimum": -90,
                "maximum": 90
              },
              "lon": {
                "type": "number",
                "minimum": -180,
                "maximum": 180
              }
            },
            "required": [
              "id"
            ],
            "additionalProperties": false
          },
          "requests": {
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
                "pickup": {
                  "type": "object",
                  "properties": {
                    "id": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 120
                    },
                    "x": {
                      "type": "number"
                    },
                    "y": {
                      "type": "number"
                    },
                    "lat": {
                      "type": "number",
                      "minimum": -90,
                      "maximum": 90
                    },
                    "lon": {
                      "type": "number",
                      "minimum": -180,
                      "maximum": 180
                    }
                  },
                  "required": [
                    "id"
                  ],
                  "additionalProperties": false
                },
                "delivery": {
                  "type": "object",
                  "properties": {
                    "id": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 120
                    },
                    "x": {
                      "type": "number"
                    },
                    "y": {
                      "type": "number"
                    },
                    "lat": {
                      "type": "number",
                      "minimum": -90,
                      "maximum": 90
                    },
                    "lon": {
                      "type": "number",
                      "minimum": -180,
                      "maximum": 180
                    }
                  },
                  "required": [
                    "id"
                  ],
                  "additionalProperties": false
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0
                }
              },
              "required": [
                "id",
                "pickup",
                "delivery",
                "quantity"
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
                "capacity": {
                  "type": "number",
                  "minimum": 0
                }
              },
              "required": [
                "id",
                "capacity"
              ],
              "additionalProperties": false
            }
          },
          "matrix": {
            "type": "object",
            "properties": {
              "distances": {
                "minItems": 1,
                "maxItems": 2000,
                "type": "array",
                "items": {
                  "type": "array",
                  "items": {
                    "type": "number"
                  }
                }
              },
              "durations": {
                "minItems": 1,
                "maxItems": 2000,
                "type": "array",
                "items": {
                  "type": "array",
                  "items": {
                    "type": "number"
                  }
                }
              }
            },
            "required": [
              "distances"
            ],
            "additionalProperties": false
          },
          "matrixFromPoints": {
            "type": "string",
            "enum": [
              "euclidean",
              "haversine"
            ]
          },
          "circuity": {
            "type": "number",
            "minimum": 1,
            "maximum": 3
          },
          "speed": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "timeLimitMs": {
            "type": "integer",
            "minimum": 1,
            "maximum": 25000
          }
        },
        "required": [
          "depot",
          "requests",
          "vehicles"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "route-optimization__multi-day-plan",
      "description": "Multi-day visit planning. Assign recurring visits across a horizon with frequency and spacing rules, then route each day. Docs: https://www.brainiac.software/api/route-optimization/multi-day-plan",
      "parameters": {
        "type": "object",
        "properties": {
          "horizonDays": {
            "minItems": 1,
            "maxItems": 28,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 120
            }
          },
          "stops": {
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
                "x": {
                  "type": "number"
                },
                "y": {
                  "type": "number"
                },
                "lat": {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90
                },
                "lon": {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180
                },
                "visitsPerWeek": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 28
                },
                "minGapDays": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 28
                },
                "allowedDays": {
                  "anyOf": [
                    {
                      "type": "array",
                      "items": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 120
                      }
                    },
                    {
                      "type": "null"
                    }
                  ]
                },
                "demand": {
                  "type": "number",
                  "minimum": 0
                }
              },
              "required": [
                "id",
                "visitsPerWeek"
              ],
              "additionalProperties": false
            }
          },
          "depot": {
            "type": "object",
            "properties": {
              "id": {
                "type": "string",
                "minLength": 1,
                "maxLength": 120
              },
              "x": {
                "type": "number"
              },
              "y": {
                "type": "number"
              },
              "lat": {
                "type": "number",
                "minimum": -90,
                "maximum": 90
              },
              "lon": {
                "type": "number",
                "minimum": -180,
                "maximum": 180
              }
            },
            "additionalProperties": false
          },
          "vehiclesPerDay": {
            "type": "integer",
            "minimum": 1,
            "maximum": 100
          },
          "capacityPerDay": {
            "anyOf": [
              {
                "type": "number",
                "minimum": 0
              },
              {
                "type": "null"
              }
            ]
          },
          "matrix": {
            "type": "object",
            "properties": {
              "distances": {
                "minItems": 1,
                "maxItems": 2000,
                "type": "array",
                "items": {
                  "type": "array",
                  "items": {
                    "type": "number"
                  }
                }
              },
              "durations": {
                "minItems": 1,
                "maxItems": 2000,
                "type": "array",
                "items": {
                  "type": "array",
                  "items": {
                    "type": "number"
                  }
                }
              }
            },
            "required": [
              "distances"
            ],
            "additionalProperties": false
          },
          "matrixFromPoints": {
            "type": "string",
            "enum": [
              "euclidean",
              "haversine"
            ]
          },
          "timeLimitMs": {
            "type": "integer",
            "minimum": 1,
            "maximum": 25000
          }
        },
        "required": [
          "horizonDays",
          "stops",
          "depot"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "route-optimization__territory-cluster",
      "description": "Balanced territory clustering. Split stops into k balanced, compact territories with capacitated k-means and imbalance limits. Docs: https://www.brainiac.software/api/route-optimization/territory-cluster",
      "parameters": {
        "type": "object",
        "properties": {
          "stops": {
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
                "x": {
                  "type": "number"
                },
                "y": {
                  "type": "number"
                },
                "lat": {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90
                },
                "lon": {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180
                },
                "weight": {
                  "type": "number",
                  "minimum": 0
                }
              },
              "required": [
                "id"
              ],
              "additionalProperties": false
            }
          },
          "k": {
            "type": "integer",
            "minimum": 1,
            "maximum": 500
          },
          "balanceBy": {
            "type": "string",
            "enum": [
              "count",
              "weight"
            ]
          },
          "maxImbalance": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
          },
          "matrixFromPoints": {
            "type": "string",
            "enum": [
              "euclidean",
              "haversine"
            ]
          },
          "seed": {
            "type": "integer",
            "minimum": -9007199254740991,
            "maximum": 9007199254740991
          }
        },
        "required": [
          "stops",
          "k"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "route-optimization__depot-location-optimize",
      "description": "Depot / hub location (p-median). Choose p hub locations from candidates to minimise demand-weighted distance, optionally capacitated. Docs: https://www.brainiac.software/api/route-optimization/depot-location-optimize",
      "parameters": {
        "type": "object",
        "properties": {
          "demand": {
            "minItems": 1,
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
                "x": {
                  "type": "number"
                },
                "y": {
                  "type": "number"
                },
                "lat": {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90
                },
                "lon": {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180
                },
                "weight": {
                  "type": "number",
                  "minimum": 0
                }
              },
              "required": [
                "id",
                "weight"
              ],
              "additionalProperties": false
            }
          },
          "candidates": {
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
                "x": {
                  "type": "number"
                },
                "y": {
                  "type": "number"
                },
                "lat": {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90
                },
                "lon": {
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
          "p": {
            "type": "integer",
            "minimum": 1,
            "maximum": 100
          },
          "matrix": {
            "type": "object",
            "properties": {
              "distances": {
                "minItems": 1,
                "maxItems": 2000,
                "type": "array",
                "items": {
                  "type": "array",
                  "items": {
                    "type": "number"
                  }
                }
              },
              "durations": {
                "minItems": 1,
                "maxItems": 2000,
                "type": "array",
                "items": {
                  "type": "array",
                  "items": {
                    "type": "number"
                  }
                }
              }
            },
            "required": [
              "distances"
            ],
            "additionalProperties": false
          },
          "matrixFromPoints": {
            "type": "string",
            "enum": [
              "euclidean",
              "haversine"
            ]
          },
          "capacities": {
            "anyOf": [
              {
                "type": "array",
                "items": {
                  "type": "number",
                  "minimum": 0
                }
              },
              {
                "type": "null"
              }
            ]
          }
        },
        "required": [
          "demand",
          "candidates",
          "p"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "route-optimization__route-eta-schedule",
      "description": "ETA schedule for a fixed sequence. Compute arrivals, waits, slack and overtime for a fixed stop sequence with optional return and shift end. Docs: https://www.brainiac.software/api/route-optimization/route-eta-schedule",
      "parameters": {
        "type": "object",
        "properties": {
          "start": {
            "type": "object",
            "properties": {
              "id": {
                "type": "string",
                "minLength": 1,
                "maxLength": 120
              },
              "x": {
                "type": "number"
              },
              "y": {
                "type": "number"
              },
              "lat": {
                "type": "number",
                "minimum": -90,
                "maximum": 90
              },
              "lon": {
                "type": "number",
                "minimum": -180,
                "maximum": 180
              },
              "time": {
                "type": "number"
              }
            },
            "required": [
              "id"
            ],
            "additionalProperties": false
          },
          "sequence": {
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
                "x": {
                  "type": "number"
                },
                "y": {
                  "type": "number"
                },
                "lat": {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90
                },
                "lon": {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180
                },
                "window": {
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
                },
                "service": {
                  "type": "number",
                  "minimum": 0
                }
              },
              "required": [
                "id"
              ],
              "additionalProperties": false
            }
          },
          "returnTo": {
            "type": "object",
            "properties": {
              "id": {
                "type": "string",
                "minLength": 1,
                "maxLength": 120
              },
              "x": {
                "type": "number"
              },
              "y": {
                "type": "number"
              },
              "lat": {
                "type": "number",
                "minimum": -90,
                "maximum": 90
              },
              "lon": {
                "type": "number",
                "minimum": -180,
                "maximum": 180
              }
            },
            "additionalProperties": false
          },
          "matrix": {
            "type": "object",
            "properties": {
              "distances": {
                "minItems": 1,
                "maxItems": 2000,
                "type": "array",
                "items": {
                  "type": "array",
                  "items": {
                    "type": "number"
                  }
                }
              },
              "durations": {
                "minItems": 1,
                "maxItems": 2000,
                "type": "array",
                "items": {
                  "type": "array",
                  "items": {
                    "type": "number"
                  }
                }
              }
            },
            "required": [
              "distances"
            ],
            "additionalProperties": false
          },
          "matrixFromPoints": {
            "type": "string",
            "enum": [
              "euclidean",
              "haversine"
            ]
          },
          "speed": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "speedMps": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "shiftEnd": {
            "type": "number"
          }
        },
        "required": [
          "start",
          "sequence"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "route-optimization__vehicle-load-sequence",
      "description": "Vehicle loading order and 3D fit. Order parcels last-delivered-first and run a deterministic layer first-fit packing check in a van or truck box. Docs: https://www.brainiac.software/api/route-optimization/vehicle-load-sequence",
      "parameters": {
        "type": "object",
        "properties": {
          "box": {
            "type": "object",
            "properties": {
              "length": {
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
              "maxWeight": {
                "type": "number",
                "exclusiveMinimum": 0
              }
            },
            "required": [
              "length",
              "width",
              "height",
              "maxWeight"
            ],
            "additionalProperties": false
          },
          "parcels": {
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
                "stopIndex": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "l": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "w": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "h": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "weight": {
                  "type": "number",
                  "minimum": 0
                },
                "rotatable": {
                  "type": "boolean"
                }
              },
              "required": [
                "id",
                "stopIndex",
                "l",
                "w",
                "h",
                "weight"
              ],
              "additionalProperties": false
            }
          },
          "units": {
            "type": "string",
            "minLength": 1,
            "maxLength": 32
          }
        },
        "required": [
          "box",
          "parcels"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "route-optimization__driver-shift-assign",
      "description": "Assign routes to drivers. Assign pre-built routes to drivers by shift, skills and vehicle type with min-cost Hungarian matching. Docs: https://www.brainiac.software/api/route-optimization/driver-shift-assign",
      "parameters": {
        "type": "object",
        "properties": {
          "routes": {
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
                "start": {
                  "type": "number"
                },
                "end": {
                  "type": "number"
                },
                "skills": {
                  "maxItems": 50,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 64
                  }
                },
                "vehicleType": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 64
                }
              },
              "required": [
                "id",
                "start",
                "end"
              ],
              "additionalProperties": false
            }
          },
          "drivers": {
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
                "shift": {
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
                },
                "skills": {
                  "maxItems": 50,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 64
                  }
                },
                "vehicleTypes": {
                  "maxItems": 50,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 64
                  }
                },
                "cost": {
                  "type": "number",
                  "minimum": 0
                }
              },
              "required": [
                "id",
                "shift"
              ],
              "additionalProperties": false
            }
          },
          "skillMode": {
            "type": "string",
            "enum": [
              "strict",
              "soft"
            ]
          },
          "skillPenalty": {
            "type": "number",
            "minimum": 0
          },
          "allowMultiple": {
            "type": "boolean"
          }
        },
        "required": [
          "routes",
          "drivers"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "route-optimization__delivery-slot-capacity",
      "description": "Delivery slot capacity. Estimate bookable orders per zone and time slot from vehicle time, service, drive and stem assumptions. Docs: https://www.brainiac.software/api/route-optimization/delivery-slot-capacity",
      "parameters": {
        "type": "object",
        "properties": {
          "zones": {
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
                "vehicles": {
                  "type": "integer",
                  "minimum": 1,
                  "maximum": 10000
                },
                "avgServiceMin": {
                  "type": "number",
                  "minimum": 0
                },
                "avgDriveBetweenStopsMin": {
                  "type": "number",
                  "minimum": 0
                },
                "stemMin": {
                  "type": "number",
                  "minimum": 0
                }
              },
              "required": [
                "id",
                "vehicles",
                "avgServiceMin",
                "avgDriveBetweenStopsMin"
              ],
              "additionalProperties": false
            }
          },
          "slots": {
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
                "start": {
                  "type": "string",
                  "pattern": "^\\d{2}:\\d{2}$"
                },
                "end": {
                  "type": "string",
                  "pattern": "^\\d{2}:\\d{2}$"
                }
              },
              "required": [
                "id",
                "start",
                "end"
              ],
              "additionalProperties": false
            }
          },
          "booked": {
            "maxItems": 50000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "zone": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "slot": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "orders": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "zone",
                "slot",
                "orders"
              ],
              "additionalProperties": false
            }
          },
          "bufferPct": {
            "type": "number",
            "minimum": 0,
            "maximum": 0.9
          },
          "stemEverySlot": {
            "type": "boolean"
          }
        },
        "required": [
          "zones",
          "slots"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "route-optimization__geofence-check",
      "description": "Geofence point-in-polygon check. Test points against GeoJSON service zones with holes, reporting inside/in-hole status and nearest boundary distance. Docs: https://www.brainiac.software/api/route-optimization/geofence-check",
      "parameters": {
        "type": "object",
        "properties": {
          "zones": {
            "type": "object",
            "properties": {
              "type": {
                "type": "string",
                "const": "FeatureCollection"
              },
              "features": {
                "minItems": 1,
                "maxItems": 1000,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "type": {
                      "type": "string",
                      "const": "Feature"
                    },
                    "properties": {
                      "type": "object",
                      "propertyNames": {
                        "type": "string"
                      },
                      "additionalProperties": {}
                    },
                    "geometry": {
                      "type": "object",
                      "properties": {
                        "type": {
                          "type": "string",
                          "enum": [
                            "Polygon",
                            "MultiPolygon"
                          ]
                        },
                        "coordinates": {
                          "type": "array",
                          "items": {}
                        }
                      },
                      "required": [
                        "type",
                        "coordinates"
                      ],
                      "additionalProperties": false
                    }
                  },
                  "required": [
                    "type",
                    "geometry"
                  ],
                  "additionalProperties": false
                }
              }
            },
            "required": [
              "type",
              "features"
            ],
            "additionalProperties": false
          },
          "points": {
            "minItems": 1,
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "lon": {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180
                },
                "lat": {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90
                }
              },
              "required": [
                "id",
                "lon",
                "lat"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "zones",
          "points"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "route-optimization__polyline-codec",
      "description": "Encoded polyline encode/decode. Encode or decode Google Encoded Polyline strings and optionally simplify with Douglas-Peucker. Docs: https://www.brainiac.software/api/route-optimization/polyline-codec",
      "parameters": {
        "type": "object",
        "properties": {
          "encode": {
            "minItems": 1,
            "maxItems": 100000,
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
          "decode": {
            "anyOf": [
              {
                "type": "string",
                "maxLength": 1000000
              },
              {
                "type": "null"
              }
            ]
          },
          "precision": {
            "anyOf": [
              {
                "type": "number",
                "const": 5
              },
              {
                "type": "number",
                "const": 6
              }
            ]
          },
          "simplify": {
            "anyOf": [
              {
                "type": "object",
                "properties": {
                  "toleranceM": {
                    "type": "number",
                    "exclusiveMinimum": 0
                  },
                  "tolerance": {
                    "type": "number",
                    "exclusiveMinimum": 0
                  }
                },
                "additionalProperties": false
              },
              {
                "type": "null"
              }
            ]
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "route-optimization__route-plan-validate",
      "description": "Validate a multi-vehicle route plan. Check a manual plan for time-window, capacity, shift, precedence and duplicate/missing-stop violations. Docs: https://www.brainiac.software/api/route-optimization/route-plan-validate",
      "parameters": {
        "type": "object",
        "properties": {
          "depot": {
            "type": "object",
            "properties": {
              "id": {
                "type": "string",
                "minLength": 1,
                "maxLength": 120
              },
              "x": {
                "type": "number"
              },
              "y": {
                "type": "number"
              },
              "lat": {
                "type": "number",
                "minimum": -90,
                "maximum": 90
              },
              "lon": {
                "type": "number",
                "minimum": -180,
                "maximum": 180
              },
              "window": {
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
            "required": [
              "id"
            ],
            "additionalProperties": false
          },
          "stops": {
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
                "x": {
                  "type": "number"
                },
                "y": {
                  "type": "number"
                },
                "lat": {
                  "type": "number",
                  "minimum": -90,
                  "maximum": 90
                },
                "lon": {
                  "type": "number",
                  "minimum": -180,
                  "maximum": 180
                },
                "window": {
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
                },
                "service": {
                  "type": "number",
                  "minimum": 0
                },
                "demand": {
                  "anyOf": [
                    {
                      "type": "number",
                      "minimum": 0
                    },
                    {
                      "minItems": 1,
                      "maxItems": 8,
                      "type": "array",
                      "items": {
                        "type": "number",
                        "minimum": 0
                      }
                    }
                  ]
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
                "shift": {
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
                },
                "capacity": {
                  "anyOf": [
                    {
                      "type": "number",
                      "minimum": 0
                    },
                    {
                      "minItems": 1,
                      "maxItems": 8,
                      "type": "array",
                      "items": {
                        "type": "number",
                        "minimum": 0
                      }
                    }
                  ]
                },
                "breaks": {
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "window": {
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
                      },
                      "duration": {
                        "type": "number",
                        "minimum": 0
                      }
                    },
                    "required": [
                      "window",
                      "duration"
                    ],
                    "additionalProperties": false
                  }
                }
              },
              "required": [
                "id"
              ],
              "additionalProperties": false
            }
          },
          "plan": {
            "minItems": 1,
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "vehicle": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "sequence": {
                  "minItems": 1,
                  "maxItems": 2000,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 120
                  }
                }
              },
              "required": [
                "vehicle",
                "sequence"
              ],
              "additionalProperties": false
            }
          },
          "requests": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "pickup": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "delivery": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 120
                },
                "quantity": {
                  "type": "number",
                  "minimum": 0
                }
              },
              "required": [
                "id",
                "pickup",
                "delivery",
                "quantity"
              ],
              "additionalProperties": false
            }
          },
          "matrix": {
            "type": "object",
            "properties": {
              "distances": {
                "minItems": 1,
                "maxItems": 2000,
                "type": "array",
                "items": {
                  "type": "array",
                  "items": {
                    "type": "number"
                  }
                }
              },
              "durations": {
                "minItems": 1,
                "maxItems": 2000,
                "type": "array",
                "items": {
                  "type": "array",
                  "items": {
                    "type": "number"
                  }
                }
              }
            },
            "required": [
              "distances"
            ],
            "additionalProperties": false
          },
          "matrixFromPoints": {
            "type": "string",
            "enum": [
              "euclidean",
              "haversine"
            ]
          },
          "speed": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "requireAllStops": {
            "type": "boolean"
          }
        },
        "required": [
          "stops",
          "vehicles",
          "plan"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "route-optimization__distance-matrix": "0.02",
  "route-optimization__tsp-optimize": "0.05",
  "route-optimization__vrp-capacitated": "0.05",
  "route-optimization__vrp-time-windows": "0.05",
  "route-optimization__pickup-delivery": "0.05",
  "route-optimization__multi-day-plan": "0.05",
  "route-optimization__territory-cluster": "0.03",
  "route-optimization__depot-location-optimize": "0.04",
  "route-optimization__route-eta-schedule": "0.02",
  "route-optimization__vehicle-load-sequence": "0.03",
  "route-optimization__driver-shift-assign": "0.03",
  "route-optimization__delivery-slot-capacity": "0.02",
  "route-optimization__geofence-check": "0.02",
  "route-optimization__polyline-codec": "0.01",
  "route-optimization__route-plan-validate": "0.02"
}
TOOL_ROUTES: Dict[str, str] = {
  "route-optimization__distance-matrix": "route-optimization/distance-matrix",
  "route-optimization__tsp-optimize": "route-optimization/tsp-optimize",
  "route-optimization__vrp-capacitated": "route-optimization/vrp-capacitated",
  "route-optimization__vrp-time-windows": "route-optimization/vrp-time-windows",
  "route-optimization__pickup-delivery": "route-optimization/pickup-delivery",
  "route-optimization__multi-day-plan": "route-optimization/multi-day-plan",
  "route-optimization__territory-cluster": "route-optimization/territory-cluster",
  "route-optimization__depot-location-optimize": "route-optimization/depot-location-optimize",
  "route-optimization__route-eta-schedule": "route-optimization/route-eta-schedule",
  "route-optimization__vehicle-load-sequence": "route-optimization/vehicle-load-sequence",
  "route-optimization__driver-shift-assign": "route-optimization/driver-shift-assign",
  "route-optimization__delivery-slot-capacity": "route-optimization/delivery-slot-capacity",
  "route-optimization__geofence-check": "route-optimization/geofence-check",
  "route-optimization__polyline-codec": "route-optimization/polyline-codec",
  "route-optimization__route-plan-validate": "route-optimization/route-plan-validate"
}


class BrainiacRouteOptimizationAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — route-optimization",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the route-optimization catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "route-optimization", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Great-circle distance and duration matrix"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.01",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the route-optimization group. "
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
