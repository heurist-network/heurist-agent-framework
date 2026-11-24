"""Auto-generated BRAINIAC Heurist Mesh agent for group `structural-calcs` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "structural-calcs__beam-analysis",
      "description": "Analyse beam reactions, shear, moment and deflection. Euler-Bernoulli FEM for simply supported, cantilever, fixed and continuous beams with point, UDL, linear and moment loads. Docs: https://www.brainiac.software/api/structural-calcs/beam-analysis",
      "parameters": {
        "type": "object",
        "properties": {
          "length": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "E": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "I": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "supports": {
            "minItems": 1,
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "x": {
                  "type": "number"
                },
                "type": {
                  "type": "string",
                  "enum": [
                    "pin",
                    "roller",
                    "fixed"
                  ]
                }
              },
              "required": [
                "x",
                "type"
              ],
              "additionalProperties": false
            }
          },
          "loads": {
            "default": [],
            "maxItems": 200,
            "type": "array",
            "items": {
              "oneOf": [
                {
                  "type": "object",
                  "properties": {
                    "type": {
                      "type": "string",
                      "const": "point"
                    },
                    "x": {
                      "type": "number"
                    },
                    "P": {
                      "type": "number"
                    }
                  },
                  "required": [
                    "type",
                    "x",
                    "P"
                  ],
                  "additionalProperties": false
                },
                {
                  "type": "object",
                  "properties": {
                    "type": {
                      "type": "string",
                      "const": "udl"
                    },
                    "w": {
                      "type": "number"
                    },
                    "from": {
                      "type": "number"
                    },
                    "to": {
                      "type": "number"
                    }
                  },
                  "required": [
                    "type",
                    "w",
                    "from",
                    "to"
                  ],
                  "additionalProperties": false
                },
                {
                  "type": "object",
                  "properties": {
                    "type": {
                      "type": "string",
                      "const": "linear"
                    },
                    "w1": {
                      "type": "number"
                    },
                    "w2": {
                      "type": "number"
                    },
                    "from": {
                      "type": "number"
                    },
                    "to": {
                      "type": "number"
                    }
                  },
                  "required": [
                    "type",
                    "w1",
                    "w2",
                    "from",
                    "to"
                  ],
                  "additionalProperties": false
                },
                {
                  "type": "object",
                  "properties": {
                    "type": {
                      "type": "string",
                      "const": "moment"
                    },
                    "x": {
                      "type": "number"
                    },
                    "M": {
                      "type": "number"
                    }
                  },
                  "required": [
                    "type",
                    "x",
                    "M"
                  ],
                  "additionalProperties": false
                }
              ]
            }
          },
          "settlements": {
            "default": [],
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "x": {
                  "type": "number"
                },
                "dy": {
                  "type": "number"
                }
              },
              "required": [
                "x",
                "dy"
              ],
              "additionalProperties": false
            }
          },
          "points": {
            "default": 61,
            "type": "integer",
            "minimum": 11,
            "maximum": 1001
          }
        },
        "required": [
          "length",
          "E",
          "I",
          "supports"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "structural-calcs__section-properties",
      "description": "Compute cross-section geometric properties. Area, centroid, second moments, elastic/plastic moduli, radii of gyration and torsion constant for standard shapes or polygons with holes. Docs: https://www.brainiac.software/api/structural-calcs/section-properties",
      "parameters": {
        "type": "object",
        "properties": {},
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "structural-calcs__column-buckling",
      "description": "Euler and Johnson column buckling. Elastic Euler and inelastic Johnson-parabola critical stress/load for a pin-ended equivalent column with caller K. Docs: https://www.brainiac.software/api/structural-calcs/column-buckling",
      "parameters": {
        "type": "object",
        "properties": {
          "E": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "fy": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "A": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "I": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "length": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "K": {
            "type": "number",
            "minimum": 0.5,
            "maximum": 10
          }
        },
        "required": [
          "E",
          "fy",
          "A",
          "I",
          "length",
          "K"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "structural-calcs__load-combinations",
      "description": "Apply load combination factors. Combine caller load-case results with caller factors and report the governing combination per result key. Docs: https://www.brainiac.software/api/structural-calcs/load-combinations",
      "parameters": {
        "type": "object",
        "properties": {
          "cases": {
            "type": "object",
            "propertyNames": {
              "type": "string",
              "minLength": 1,
              "maxLength": 40
            },
            "additionalProperties": {
              "type": "object",
              "propertyNames": {
                "type": "string",
                "minLength": 1,
                "maxLength": 40
              },
              "additionalProperties": {
                "type": "number"
              }
            }
          },
          "combinations": {
            "minItems": 1,
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "factors": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 40
                  },
                  "additionalProperties": {
                    "type": "number"
                  }
                }
              },
              "required": [
                "name",
                "factors"
              ],
              "additionalProperties": false
            }
          },
          "governBy": {
            "default": "absolute",
            "type": "string",
            "enum": [
              "absolute",
              "max",
              "min"
            ]
          }
        },
        "required": [
          "cases",
          "combinations"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "structural-calcs__truss-2d-analysis",
      "description": "Analyse a 2D pin-jointed truss. Direct-stiffness truss analysis returning member axial forces, support reactions and joint displacements. Docs: https://www.brainiac.software/api/structural-calcs/truss-2d-analysis",
      "parameters": {
        "type": "object",
        "properties": {
          "nodes": {
            "minItems": 2,
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "x": {
                  "type": "number"
                },
                "y": {
                  "type": "number"
                },
                "support": {
                  "anyOf": [
                    {
                      "type": "string",
                      "enum": [
                        "pin",
                        "roller_x",
                        "roller_y",
                        "fixed"
                      ]
                    },
                    {
                      "type": "object",
                      "properties": {
                        "dx": {
                          "type": "boolean"
                        },
                        "dy": {
                          "type": "boolean"
                        }
                      },
                      "required": [
                        "dx",
                        "dy"
                      ],
                      "additionalProperties": false
                    }
                  ]
                }
              },
              "required": [
                "id",
                "x",
                "y"
              ],
              "additionalProperties": false
            }
          },
          "members": {
            "minItems": 1,
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "i": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "j": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "E": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "A": {
                  "type": "number",
                  "exclusiveMinimum": 0
                }
              },
              "required": [
                "id",
                "i",
                "j",
                "E",
                "A"
              ],
              "additionalProperties": false
            }
          },
          "loads": {
            "default": [],
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "node": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "Fx": {
                  "default": 0,
                  "type": "number"
                },
                "Fy": {
                  "default": 0,
                  "type": "number"
                }
              },
              "required": [
                "node"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "nodes",
          "members"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "structural-calcs__frame-2d-analysis",
      "description": "Analyse a 2D frame. Euler-Bernoulli frame analysis with optional moment releases, nodal and member loads, returning displacements, reactions and member end forces. Docs: https://www.brainiac.software/api/structural-calcs/frame-2d-analysis",
      "parameters": {
        "type": "object",
        "properties": {
          "nodes": {
            "minItems": 2,
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "x": {
                  "type": "number"
                },
                "y": {
                  "type": "number"
                },
                "support": {
                  "anyOf": [
                    {
                      "type": "string",
                      "enum": [
                        "pin",
                        "roller_x",
                        "roller_y",
                        "fixed"
                      ]
                    },
                    {
                      "type": "object",
                      "properties": {
                        "dx": {
                          "type": "boolean"
                        },
                        "dy": {
                          "type": "boolean"
                        },
                        "rz": {
                          "type": "boolean"
                        }
                      },
                      "required": [
                        "dx",
                        "dy",
                        "rz"
                      ],
                      "additionalProperties": false
                    }
                  ]
                }
              },
              "required": [
                "id",
                "x",
                "y"
              ],
              "additionalProperties": false
            }
          },
          "members": {
            "minItems": 1,
            "maxItems": 5000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "i": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "j": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "E": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "A": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "I": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "releaseI": {
                  "default": false,
                  "type": "boolean"
                },
                "releaseJ": {
                  "default": false,
                  "type": "boolean"
                }
              },
              "required": [
                "id",
                "i",
                "j",
                "E",
                "A",
                "I"
              ],
              "additionalProperties": false
            }
          },
          "nodalLoads": {
            "default": [],
            "maxItems": 2000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "node": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "Fx": {
                  "default": 0,
                  "type": "number"
                },
                "Fy": {
                  "default": 0,
                  "type": "number"
                },
                "Mz": {
                  "default": 0,
                  "type": "number"
                }
              },
              "required": [
                "node"
              ],
              "additionalProperties": false
            }
          },
          "memberLoads": {
            "default": [],
            "maxItems": 2000,
            "type": "array",
            "items": {
              "oneOf": [
                {
                  "type": "object",
                  "properties": {
                    "member": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 40
                    },
                    "type": {
                      "type": "string",
                      "const": "udl"
                    },
                    "w": {
                      "type": "number"
                    },
                    "axes": {
                      "default": "local",
                      "type": "string",
                      "enum": [
                        "local",
                        "global"
                      ]
                    },
                    "direction": {
                      "default": "y",
                      "type": "string",
                      "enum": [
                        "y",
                        "x"
                      ]
                    }
                  },
                  "required": [
                    "member",
                    "type",
                    "w"
                  ],
                  "additionalProperties": false
                },
                {
                  "type": "object",
                  "properties": {
                    "member": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 40
                    },
                    "type": {
                      "type": "string",
                      "const": "point"
                    },
                    "P": {
                      "type": "number"
                    },
                    "a": {
                      "type": "number",
                      "minimum": 0
                    },
                    "axes": {
                      "default": "local",
                      "type": "string",
                      "enum": [
                        "local",
                        "global"
                      ]
                    },
                    "direction": {
                      "default": "y",
                      "type": "string",
                      "enum": [
                        "y",
                        "x"
                      ]
                    }
                  },
                  "required": [
                    "member",
                    "type",
                    "P",
                    "a"
                  ],
                  "additionalProperties": false
                }
              ]
            }
          }
        },
        "required": [
          "nodes",
          "members"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "structural-calcs__bolt-group-eccentric",
      "description": "Eccentric bolt-group forces (elastic). Elastic-method force distribution in an in-plane eccentrically loaded bolt group. Docs: https://www.brainiac.software/api/structural-calcs/bolt-group-eccentric",
      "parameters": {
        "type": "object",
        "properties": {
          "bolts": {
            "minItems": 2,
            "maxItems": 500,
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
          "load": {
            "type": "object",
            "properties": {
              "Px": {
                "type": "number"
              },
              "Py": {
                "type": "number"
              },
              "x": {
                "type": "number"
              },
              "y": {
                "type": "number"
              }
            },
            "required": [
              "Px",
              "Py",
              "x",
              "y"
            ],
            "additionalProperties": false
          }
        },
        "required": [
          "bolts",
          "load"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "structural-calcs__weld-group-analysis",
      "description": "Eccentric weld-group force per length. Elastic line-weld analysis of an eccentrically loaded weld group returning maximum force per unit length. Docs: https://www.brainiac.software/api/structural-calcs/weld-group-analysis",
      "parameters": {
        "type": "object",
        "properties": {
          "lines": {
            "minItems": 1,
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "from": {
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
                "to": {
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
                "from",
                "to"
              ],
              "additionalProperties": false
            }
          },
          "load": {
            "type": "object",
            "properties": {
              "Px": {
                "type": "number"
              },
              "Py": {
                "type": "number"
              },
              "x": {
                "type": "number"
              },
              "y": {
                "type": "number"
              }
            },
            "required": [
              "Px",
              "Py",
              "x",
              "y"
            ],
            "additionalProperties": false
          }
        },
        "required": [
          "lines",
          "load"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "structural-calcs__footing-bearing-pressure",
      "description": "Spread-footing bearing pressure. Soil bearing pressure under a rectangular footing with axial load and moments, including partial uplift. Docs: https://www.brainiac.software/api/structural-calcs/footing-bearing-pressure",
      "parameters": {
        "type": "object",
        "properties": {
          "B": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "L": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "P": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "Mx": {
            "default": 0,
            "type": "number"
          },
          "My": {
            "default": 0,
            "type": "number"
          }
        },
        "required": [
          "B",
          "L",
          "P"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "structural-calcs__retaining-wall-stability",
      "description": "Cantilever retaining-wall stability. Overturning, sliding and bearing checks for a cantilever retaining wall with Rankine or Coulomb active pressure. Docs: https://www.brainiac.software/api/structural-calcs/retaining-wall-stability",
      "parameters": {
        "type": "object",
        "properties": {
          "geometry": {
            "type": "object",
            "properties": {
              "totalHeight": {
                "type": "number",
                "exclusiveMinimum": 0
              },
              "baseThickness": {
                "type": "number",
                "exclusiveMinimum": 0
              },
              "baseWidth": {
                "type": "number",
                "exclusiveMinimum": 0
              },
              "toe": {
                "type": "number",
                "minimum": 0
              },
              "stemThickness": {
                "type": "number",
                "exclusiveMinimum": 0
              }
            },
            "required": [
              "totalHeight",
              "baseThickness",
              "baseWidth",
              "toe",
              "stemThickness"
            ],
            "additionalProperties": false
          },
          "soil": {
            "type": "object",
            "properties": {
              "gamma": {
                "type": "number",
                "exclusiveMinimum": 0
              },
              "phi": {
                "type": "number",
                "minimum": 10,
                "maximum": 50
              },
              "cohesion": {
                "default": 0,
                "type": "number",
                "minimum": 0
              }
            },
            "required": [
              "gamma",
              "phi"
            ],
            "additionalProperties": false
          },
          "concreteGamma": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "baseFriction": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "surcharge": {
            "default": 0,
            "type": "number",
            "minimum": 0
          },
          "theory": {
            "default": "rankine",
            "type": "string",
            "enum": [
              "rankine",
              "coulomb"
            ]
          },
          "wallFriction": {
            "type": "number",
            "minimum": 0,
            "maximum": 40
          },
          "waterTableDepth": {
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
          "passiveIgnored": {
            "default": true,
            "type": "boolean"
          }
        },
        "required": [
          "geometry",
          "soil",
          "concreteGamma",
          "baseFriction"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "structural-calcs__concrete-rect-flexure",
      "description": "Rectangular concrete section flexure. Nominal flexural strength of a singly or doubly reinforced rectangular section with caller stress-block parameters. Docs: https://www.brainiac.software/api/structural-calcs/concrete-rect-flexure",
      "parameters": {
        "type": "object",
        "properties": {
          "b": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "d": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "As": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "fc": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "fy": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "Es": {
            "default": 200000,
            "type": "number",
            "exclusiveMinimum": 0
          },
          "beta1": {
            "type": "number",
            "exclusiveMinimum": 0,
            "maximum": 1
          },
          "alpha1": {
            "type": "number",
            "exclusiveMinimum": 0,
            "maximum": 1.5
          },
          "epsCu": {
            "type": "number",
            "exclusiveMinimum": 0,
            "maximum": 0.01
          },
          "AsPrime": {
            "default": 0,
            "type": "number",
            "minimum": 0
          },
          "dPrime": {
            "default": 0,
            "type": "number",
            "minimum": 0
          },
          "phi": {
            "anyOf": [
              {
                "type": "number",
                "minimum": 0,
                "maximum": 1
              },
              {
                "type": "null"
              }
            ]
          }
        },
        "required": [
          "b",
          "d",
          "As",
          "fc",
          "fy",
          "beta1",
          "alpha1",
          "epsCu"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "structural-calcs__composite-section-transform",
      "description": "Transformed composite section properties. Modular-ratio transformed-section properties and stresses for multi-material sections, optionally cracked. Docs: https://www.brainiac.software/api/structural-calcs/composite-section-transform",
      "parameters": {
        "type": "object",
        "properties": {
          "reference": {
            "type": "string",
            "minLength": 1,
            "maxLength": 40
          },
          "parts": {
            "minItems": 2,
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "shape": {
                  "type": "string",
                  "enum": [
                    "rectangle",
                    "polygon"
                  ]
                },
                "b": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "h": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "y0": {
                  "default": 0,
                  "type": "number"
                },
                "x0": {
                  "default": 0,
                  "type": "number"
                },
                "E": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "outer": {
                  "minItems": 3,
                  "maxItems": 500,
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
                "isConcrete": {
                  "default": false,
                  "type": "boolean"
                }
              },
              "required": [
                "name",
                "shape",
                "E"
              ],
              "additionalProperties": false
            }
          },
          "moment": {
            "default": 0,
            "type": "number"
          },
          "concreteCracked": {
            "default": false,
            "type": "boolean"
          }
        },
        "required": [
          "reference",
          "parts"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "structural-calcs__deflection-limit-check",
      "description": "Check deflections against span ratios. Compare computed deflections with caller span/deflection limits and optional long-term multipliers. Docs: https://www.brainiac.software/api/structural-calcs/deflection-limit-check",
      "parameters": {
        "type": "object",
        "properties": {
          "span": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "checks": {
            "minItems": 1,
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "case": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "deflection": {
                  "type": "number"
                },
                "limitRatio": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "multiplier": {
                  "default": 1,
                  "type": "number",
                  "exclusiveMinimum": 0
                }
              },
              "required": [
                "case",
                "deflection",
                "limitRatio"
              ],
              "additionalProperties": false
            }
          },
          "absoluteLimit": {
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
          "span",
          "checks"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "structural-calcs__tributary-load-takedown",
      "description": "Column tributary areas and load takedown. Tributary areas on a rectangular grid (or caller polygons) with cumulative dead/live takedown over floors. Docs: https://www.brainiac.software/api/structural-calcs/tributary-load-takedown",
      "parameters": {
        "type": "object",
        "properties": {
          "gridX": {
            "minItems": 2,
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "number"
            }
          },
          "gridY": {
            "minItems": 2,
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "number"
            }
          },
          "floors": {
            "minItems": 1,
            "maxItems": 200,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "dead": {
                  "type": "number",
                  "minimum": 0
                },
                "live": {
                  "type": "number",
                  "minimum": 0
                }
              },
              "required": [
                "name",
                "dead",
                "live"
              ],
              "additionalProperties": false
            }
          },
          "factors": {
            "anyOf": [
              {
                "type": "object",
                "properties": {
                  "dead": {
                    "type": "number"
                  },
                  "live": {
                    "type": "number"
                  }
                },
                "required": [
                  "dead",
                  "live"
                ],
                "additionalProperties": false
              },
              {
                "type": "null"
              }
            ]
          },
          "omittedColumns": {
            "default": [],
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 40
            }
          },
          "columns": {
            "maxItems": 500,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 40
                },
                "x": {
                  "type": "number"
                },
                "y": {
                  "type": "number"
                },
                "polygon": {
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
                "tributaryArea": {
                  "type": "number",
                  "exclusiveMinimum": 0
                }
              },
              "required": [
                "id"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "floors"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "structural-calcs__beam-analysis": "0.04",
  "structural-calcs__section-properties": "0.03",
  "structural-calcs__column-buckling": "0.02",
  "structural-calcs__load-combinations": "0.01",
  "structural-calcs__truss-2d-analysis": "0.04",
  "structural-calcs__frame-2d-analysis": "0.05",
  "structural-calcs__bolt-group-eccentric": "0.02",
  "structural-calcs__weld-group-analysis": "0.02",
  "structural-calcs__footing-bearing-pressure": "0.03",
  "structural-calcs__retaining-wall-stability": "0.03",
  "structural-calcs__concrete-rect-flexure": "0.03",
  "structural-calcs__composite-section-transform": "0.03",
  "structural-calcs__deflection-limit-check": "0.01",
  "structural-calcs__tributary-load-takedown": "0.02"
}
TOOL_ROUTES: Dict[str, str] = {
  "structural-calcs__beam-analysis": "structural-calcs/beam-analysis",
  "structural-calcs__section-properties": "structural-calcs/section-properties",
  "structural-calcs__column-buckling": "structural-calcs/column-buckling",
  "structural-calcs__load-combinations": "structural-calcs/load-combinations",
  "structural-calcs__truss-2d-analysis": "structural-calcs/truss-2d-analysis",
  "structural-calcs__frame-2d-analysis": "structural-calcs/frame-2d-analysis",
  "structural-calcs__bolt-group-eccentric": "structural-calcs/bolt-group-eccentric",
  "structural-calcs__weld-group-analysis": "structural-calcs/weld-group-analysis",
  "structural-calcs__footing-bearing-pressure": "structural-calcs/footing-bearing-pressure",
  "structural-calcs__retaining-wall-stability": "structural-calcs/retaining-wall-stability",
  "structural-calcs__concrete-rect-flexure": "structural-calcs/concrete-rect-flexure",
  "structural-calcs__composite-section-transform": "structural-calcs/composite-section-transform",
  "structural-calcs__deflection-limit-check": "structural-calcs/deflection-limit-check",
  "structural-calcs__tributary-load-takedown": "structural-calcs/tributary-load-takedown"
}


class BrainiacStructuralCalcsAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — structural-calcs",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the structural-calcs catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "structural-calcs", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Analyse beam reactions, shear, moment and deflection"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.01",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the structural-calcs group. "
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
