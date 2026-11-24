"""Auto-generated BRAINIAC Heurist Mesh agent for group `experimentation` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "experimentation__ab-test-frequentist",
      "description": "Run a frequentist A/B test scorecard. Two-arm A/B scorecard for conversion (two-proportion z) or continuous (Welch t) metrics: absolute and relative lift, confidence intervals, p-value and significance. Pure computation on supplied aggregates. Docs: https://www.brainiac.software/api/experimentation/ab-test-frequentist",
      "parameters": {
        "type": "object",
        "properties": {
          "metricType": {
            "type": "string",
            "enum": [
              "proportion",
              "mean"
            ]
          },
          "alpha": {
            "default": 0.05,
            "type": "number",
            "exclusiveMinimum": 0,
            "exclusiveMaximum": 0.5
          },
          "alternative": {
            "default": "two-sided",
            "type": "string",
            "enum": [
              "two-sided",
              "greater",
              "less"
            ]
          },
          "control": {
            "anyOf": [
              {
                "type": "object",
                "properties": {
                  "users": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 9007199254740991
                  },
                  "conversions": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 9007199254740991
                  }
                },
                "required": [
                  "users",
                  "conversions"
                ],
                "additionalProperties": false
              },
              {
                "type": "object",
                "properties": {
                  "n": {
                    "type": "integer",
                    "minimum": 2,
                    "maximum": 9007199254740991
                  },
                  "mean": {
                    "type": "number"
                  },
                  "sd": {
                    "type": "number",
                    "minimum": 0
                  }
                },
                "required": [
                  "n",
                  "mean",
                  "sd"
                ],
                "additionalProperties": false
              }
            ]
          },
          "treatment": {
            "anyOf": [
              {
                "type": "object",
                "properties": {
                  "users": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 9007199254740991
                  },
                  "conversions": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 9007199254740991
                  }
                },
                "required": [
                  "users",
                  "conversions"
                ],
                "additionalProperties": false
              },
              {
                "type": "object",
                "properties": {
                  "n": {
                    "type": "integer",
                    "minimum": 2,
                    "maximum": 9007199254740991
                  },
                  "mean": {
                    "type": "number"
                  },
                  "sd": {
                    "type": "number",
                    "minimum": 0
                  }
                },
                "required": [
                  "n",
                  "mean",
                  "sd"
                ],
                "additionalProperties": false
              }
            ]
          }
        },
        "required": [
          "metricType",
          "control",
          "treatment"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "experimentation__bayesian-ab",
      "description": "Compare A/B arms with a Bayesian Beta-Binomial model. Posterior, probability to beat control, probability of being best, expected loss and equal-tailed credible intervals for 2-10 conversion arms. Deterministic: exact Miller sum or quadrature, no Monte Carlo. Docs: https://www.brainiac.software/api/experimentation/bayesian-ab",
      "parameters": {
        "type": "object",
        "properties": {
          "prior": {
            "default": {
              "alpha": 1,
              "beta": 1
            },
            "type": "object",
            "properties": {
              "alpha": {
                "default": 1,
                "type": "number",
                "exclusiveMinimum": 0
              },
              "beta": {
                "default": 1,
                "type": "number",
                "exclusiveMinimum": 0
              }
            },
            "additionalProperties": false
          },
          "arms": {
            "minItems": 2,
            "maxItems": 10,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 64
                },
                "control": {
                  "type": "boolean"
                },
                "users": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "conversions": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "name",
                "users",
                "conversions"
              ],
              "additionalProperties": false
            }
          },
          "credibleLevel": {
            "default": 0.95,
            "type": "number",
            "exclusiveMinimum": 0.5,
            "exclusiveMaximum": 0.999
          }
        },
        "required": [
          "arms"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "experimentation__sequential-test",
      "description": "Compute sequential testing boundaries or an always-valid p-value. Lan-DeMets group-sequential boundaries (O'Brien-Fleming or Pocock spending) for planned looks with a stop/continue decision, or an always-valid mSPRT p-value for continuous monitoring. Docs: https://www.brainiac.software/api/experimentation/sequential-test",
      "parameters": {
        "type": "object",
        "properties": {
          "mode": {
            "type": "string",
            "enum": [
              "group_sequential",
              "msprt"
            ]
          },
          "alpha": {
            "default": 0.05,
            "type": "number",
            "exclusiveMinimum": 0,
            "exclusiveMaximum": 0.5
          },
          "spending": {
            "default": "obrien_fleming",
            "type": "string",
            "enum": [
              "obrien_fleming",
              "pocock"
            ]
          },
          "informationFractions": {
            "minItems": 1,
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "number",
              "exclusiveMinimum": 0,
              "maximum": 1
            }
          },
          "observedZ": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": [
                "number",
                "null"
              ]
            }
          },
          "estimate": {
            "type": "number"
          },
          "variance": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "tau2": {
            "type": "number",
            "exclusiveMinimum": 0
          }
        },
        "required": [
          "mode"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "experimentation__cuped-adjust",
      "description": "Apply CUPED variance reduction and test the adjusted effect. CUPED adjustment with a pre-experiment covariate on unit-level data: theta, variance reduction, and Welch tests on raw and adjusted values. Docs: https://www.brainiac.software/api/experimentation/cuped-adjust",
      "parameters": {
        "type": "object",
        "properties": {
          "units": {
            "minItems": 4,
            "maxItems": 200000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "group": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 64
                },
                "y": {
                  "type": "number"
                },
                "x": {
                  "type": [
                    "number",
                    "null"
                  ]
                }
              },
              "required": [
                "group",
                "y"
              ],
              "additionalProperties": false
            }
          },
          "alpha": {
            "default": 0.05,
            "type": "number",
            "exclusiveMinimum": 0,
            "exclusiveMaximum": 0.5
          }
        },
        "required": [
          "units"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "experimentation__sample-ratio-mismatch",
      "description": "Detect A/B sample ratio mismatch. Chi-square goodness-of-fit test of observed arm counts against expected traffic shares, with an exact binomial p-value for tiny two-arm counts and generic causes when a mismatch is flagged. Docs: https://www.brainiac.software/api/experimentation/sample-ratio-mismatch",
      "parameters": {
        "type": "object",
        "properties": {
          "arms": {
            "minItems": 2,
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 64
                },
                "observed": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "expectedShare": {
                  "type": "number",
                  "exclusiveMinimum": 0,
                  "maximum": 1
                }
              },
              "required": [
                "name",
                "observed",
                "expectedShare"
              ],
              "additionalProperties": false
            }
          },
          "threshold": {
            "default": 0.0005,
            "type": "number",
            "exclusiveMinimum": 0,
            "exclusiveMaximum": 1
          }
        },
        "required": [
          "arms"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "experimentation__sample-size-mde",
      "description": "Calculate A/B sample size or minimum detectable effect. Required users per arm and duration for a target minimum detectable effect, or the MDE for a fixed sample, for proportion or mean metrics with power, multi-arm Bonferroni and unequal allocation. Docs: https://www.brainiac.software/api/experimentation/sample-size-mde",
      "parameters": {
        "type": "object",
        "properties": {
          "metricType": {
            "type": "string",
            "enum": [
              "proportion",
              "mean"
            ]
          },
          "baseline": {
            "type": "number",
            "exclusiveMinimum": 0,
            "exclusiveMaximum": 1
          },
          "baselineSd": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "baselineMean": {
            "type": "number"
          },
          "mde": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "mdeType": {
            "default": "relative",
            "type": "string",
            "enum": [
              "relative",
              "absolute"
            ]
          },
          "nPerArm": {
            "type": "integer",
            "minimum": 2,
            "maximum": 9007199254740991
          },
          "alpha": {
            "default": 0.05,
            "type": "number",
            "exclusiveMinimum": 0,
            "exclusiveMaximum": 0.5
          },
          "alternative": {
            "default": "two-sided",
            "type": "string",
            "enum": [
              "two-sided",
              "greater",
              "less"
            ]
          },
          "power": {
            "default": 0.8,
            "type": "number",
            "exclusiveMinimum": 0.5,
            "exclusiveMaximum": 0.999
          },
          "arms": {
            "default": 2,
            "type": "integer",
            "minimum": 2,
            "maximum": 10
          },
          "allocation": {
            "minItems": 2,
            "maxItems": 10,
            "type": "array",
            "items": {
              "type": "number",
              "exclusiveMinimum": 0,
              "exclusiveMaximum": 1
            }
          },
          "dailyUsers": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "correction": {
            "default": "none",
            "type": "string",
            "enum": [
              "bonferroni",
              "none"
            ]
          }
        },
        "required": [
          "metricType"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "experimentation__multiple-testing-correct",
      "description": "Adjust p-values for multiple testing. Bonferroni, Holm and Benjamini-Hochberg adjusted p-values and reject decisions across metrics or arms, returned in input order. Docs: https://www.brainiac.software/api/experimentation/multiple-testing-correct",
      "parameters": {
        "type": "object",
        "properties": {
          "pValues": {
            "minItems": 1,
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 64
                },
                "p": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1
                }
              },
              "required": [
                "id",
                "p"
              ],
              "additionalProperties": false
            }
          },
          "methods": {
            "default": [
              "bonferroni",
              "holm",
              "benjamini_hochberg"
            ],
            "minItems": 1,
            "maxItems": 3,
            "type": "array",
            "items": {
              "type": "string",
              "enum": [
                "bonferroni",
                "holm",
                "benjamini_hochberg"
              ]
            }
          },
          "alpha": {
            "default": 0.05,
            "type": "number",
            "exclusiveMinimum": 0,
            "exclusiveMaximum": 0.5
          }
        },
        "required": [
          "pValues"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "experimentation__delta-method-ratio",
      "description": "Estimate a ratio metric with the delta method. Confidence interval for a ratio metric whose analysis unit differs from the randomisation unit, plus the treatment-vs-control difference and relative lift. Accepts unit rows or aggregates. Docs: https://www.brainiac.software/api/experimentation/delta-method-ratio",
      "parameters": {
        "type": "object",
        "properties": {
          "arms": {
            "minItems": 1,
            "maxItems": 2,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 64
                },
                "control": {
                  "type": "boolean"
                },
                "units": {
                  "minItems": 2,
                  "maxItems": 1000000,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "num": {
                        "type": "number"
                      },
                      "den": {
                        "type": "number",
                        "minimum": 0
                      }
                    },
                    "required": [
                      "num",
                      "den"
                    ],
                    "additionalProperties": false
                  }
                },
                "n": {
                  "type": "integer",
                  "minimum": 2,
                  "maximum": 9007199254740991
                },
                "sumNum": {
                  "type": "number"
                },
                "sumDen": {
                  "type": "number",
                  "minimum": 0
                },
                "sumNum2": {
                  "type": "number",
                  "minimum": 0
                },
                "sumDen2": {
                  "type": "number",
                  "minimum": 0
                },
                "sumNumDen": {
                  "type": "number"
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "alpha": {
            "default": 0.05,
            "type": "number",
            "exclusiveMinimum": 0,
            "exclusiveMaximum": 0.5
          }
        },
        "required": [
          "arms"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "experimentation__bandit-allocate",
      "description": "Compute multi-armed bandit traffic weights. Next-period traffic weights from arm outcomes: Thompson-sampling probabilities by deterministic quadrature, or UCB1 indices, with an exploration floor. Docs: https://www.brainiac.software/api/experimentation/bandit-allocate",
      "parameters": {
        "type": "object",
        "properties": {
          "policy": {
            "type": "string",
            "enum": [
              "thompson",
              "ucb1"
            ]
          },
          "arms": {
            "minItems": 2,
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 64
                },
                "successes": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "failures": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                }
              },
              "required": [
                "name",
                "successes",
                "failures"
              ],
              "additionalProperties": false
            }
          },
          "prior": {
            "default": {
              "alpha": 1,
              "beta": 1
            },
            "type": "object",
            "properties": {
              "alpha": {
                "default": 1,
                "type": "number",
                "exclusiveMinimum": 0
              },
              "beta": {
                "default": 1,
                "type": "number",
                "exclusiveMinimum": 0
              }
            },
            "additionalProperties": false
          },
          "minShare": {
            "default": 0,
            "type": "number",
            "minimum": 0,
            "maximum": 0.5
          }
        },
        "required": [
          "policy",
          "arms"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "experimentation__bucket-assign",
      "description": "Assign units to experiment groups deterministically. Stateless SHA-256 bucketing of unit ids into an experiment with traffic gating, ordered group shares and an optional layer, documented so any SDK can reproduce it. Docs: https://www.brainiac.software/api/experimentation/bucket-assign",
      "parameters": {
        "type": "object",
        "properties": {
          "unitIds": {
            "minItems": 1,
            "maxItems": 10000,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 256
            }
          },
          "experiment": {
            "type": "object",
            "properties": {
              "name": {
                "type": "string",
                "minLength": 1,
                "maxLength": 128
              },
              "salt": {
                "type": "string",
                "minLength": 1,
                "maxLength": 128
              },
              "trafficShare": {
                "default": 1,
                "type": "number",
                "exclusiveMinimum": 0,
                "maximum": 1
              },
              "groups": {
                "minItems": 1,
                "maxItems": 20,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "name": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 64
                    },
                    "share": {
                      "type": "number",
                      "exclusiveMinimum": 0,
                      "maximum": 1
                    }
                  },
                  "required": [
                    "name",
                    "share"
                  ],
                  "additionalProperties": false
                }
              }
            },
            "required": [
              "salt",
              "groups"
            ],
            "additionalProperties": false
          },
          "layer": {
            "anyOf": [
              {
                "type": "object",
                "properties": {
                  "salt": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 128
                  },
                  "segments": {
                    "minItems": 1,
                    "maxItems": 100,
                    "type": "array",
                    "items": {
                      "type": "object",
                      "properties": {
                        "experiment": {
                          "type": "string",
                          "minLength": 1,
                          "maxLength": 128
                        },
                        "from": {
                          "type": "integer",
                          "minimum": 0,
                          "maximum": 9999
                        },
                        "to": {
                          "type": "integer",
                          "minimum": 1,
                          "maximum": 10000
                        }
                      },
                      "required": [
                        "experiment",
                        "from",
                        "to"
                      ],
                      "additionalProperties": false
                    }
                  }
                },
                "required": [
                  "salt",
                  "segments"
                ],
                "additionalProperties": false
              },
              {
                "type": "null"
              }
            ]
          }
        },
        "required": [
          "unitIds",
          "experiment"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "experimentation__flag-rule-evaluate",
      "description": "Evaluate a feature-flag rule set. Evaluate ordered feature-flag rules (attribute operators, semver comparison, deterministic percentage rollout) for one user context and explain which rule matched. Docs: https://www.brainiac.software/api/experimentation/flag-rule-evaluate",
      "parameters": {
        "type": "object",
        "properties": {
          "flag": {
            "type": "object",
            "properties": {
              "key": {
                "type": "string",
                "minLength": 1,
                "maxLength": 128
              },
              "salt": {
                "type": "string",
                "minLength": 1,
                "maxLength": 128
              },
              "default": {
                "type": [
                  "string",
                  "number",
                  "boolean"
                ]
              },
              "rules": {
                "maxItems": 100,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "id": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 64
                    },
                    "conditions": {
                      "default": [],
                      "maxItems": 20,
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "attribute": {
                            "type": "string",
                            "minLength": 1,
                            "maxLength": 128
                          },
                          "op": {
                            "type": "string",
                            "enum": [
                              "eq",
                              "neq",
                              "in",
                              "not_in",
                              "contains",
                              "starts_with",
                              "ends_with",
                              "regex",
                              "gt",
                              "gte",
                              "lt",
                              "lte",
                              "semver_gt",
                              "semver_gte",
                              "semver_lt",
                              "semver_lte",
                              "exists"
                            ]
                          },
                          "value": {
                            "anyOf": [
                              {
                                "type": [
                                  "string",
                                  "number",
                                  "boolean"
                                ]
                              },
                              {
                                "maxItems": 1000,
                                "type": "array",
                                "items": {
                                  "type": [
                                    "string",
                                    "number"
                                  ]
                                }
                              }
                            ]
                          }
                        },
                        "required": [
                          "attribute",
                          "op"
                        ],
                        "additionalProperties": false
                      }
                    },
                    "rollout": {
                      "type": "number",
                      "minimum": 0,
                      "maximum": 1
                    },
                    "serve": {
                      "type": [
                        "string",
                        "number",
                        "boolean"
                      ]
                    }
                  },
                  "required": [
                    "id",
                    "serve"
                  ],
                  "additionalProperties": false
                }
              }
            },
            "required": [
              "key",
              "salt",
              "default",
              "rules"
            ],
            "additionalProperties": false
          },
          "context": {
            "type": "object",
            "propertyNames": {
              "type": "string"
            },
            "additionalProperties": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "number"
                },
                {
                  "type": "boolean"
                },
                {
                  "type": "null"
                },
                {
                  "maxItems": 1000,
                  "type": "array",
                  "items": {
                    "type": [
                      "string",
                      "number"
                    ]
                  }
                }
              ]
            }
          }
        },
        "required": [
          "flag",
          "context"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "experimentation__novelty-effect-detect",
      "description": "Detect novelty or primacy effects in daily lift. OLS trend test on daily lift with early-versus-late means, classifying the pattern as novelty, primacy or stable. Docs: https://www.brainiac.software/api/experimentation/novelty-effect-detect",
      "parameters": {
        "type": "object",
        "properties": {
          "daily": {
            "minItems": 6,
            "maxItems": 365,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "day": {
                  "type": "number"
                },
                "lift": {
                  "type": "number"
                }
              },
              "required": [
                "day",
                "lift"
              ],
              "additionalProperties": false
            }
          },
          "liftType": {
            "type": "string",
            "enum": [
              "relative",
              "absolute"
            ]
          },
          "earlyDays": {
            "type": "integer",
            "minimum": 1,
            "maximum": 9007199254740991
          },
          "alpha": {
            "default": 0.05,
            "type": "number",
            "exclusiveMinimum": 0,
            "exclusiveMaximum": 0.5
          }
        },
        "required": [
          "daily"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "experimentation__segment-lift",
      "description": "Measure A/B lift per segment with FDR control. Per-segment conversion lift with Benjamini-Hochberg adjusted p-values, a Cochran Q heterogeneity test and suppression of small segments. Docs: https://www.brainiac.software/api/experimentation/segment-lift",
      "parameters": {
        "type": "object",
        "properties": {
          "segments": {
            "minItems": 1,
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 64
                },
                "control": {
                  "type": "object",
                  "properties": {
                    "users": {
                      "type": "integer",
                      "minimum": 1,
                      "maximum": 9007199254740991
                    },
                    "conversions": {
                      "type": "integer",
                      "minimum": 0,
                      "maximum": 9007199254740991
                    }
                  },
                  "required": [
                    "users",
                    "conversions"
                  ],
                  "additionalProperties": false
                },
                "treatment": {
                  "type": "object",
                  "properties": {
                    "users": {
                      "type": "integer",
                      "minimum": 1,
                      "maximum": 9007199254740991
                    },
                    "conversions": {
                      "type": "integer",
                      "minimum": 0,
                      "maximum": 9007199254740991
                    }
                  },
                  "required": [
                    "users",
                    "conversions"
                  ],
                  "additionalProperties": false
                }
              },
              "required": [
                "name",
                "control",
                "treatment"
              ],
              "additionalProperties": false
            }
          },
          "minUsersPerArm": {
            "default": 100,
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          },
          "alpha": {
            "default": 0.05,
            "type": "number",
            "exclusiveMinimum": 0,
            "exclusiveMaximum": 0.5
          }
        },
        "required": [
          "segments"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "experimentation__guardrail-check",
      "description": "Check A/B guardrail metrics for non-inferiority. One-sided non-inferiority tests of guardrail metrics against caller-supplied relative or absolute margins, with bounds and an overall pass flag. Docs: https://www.brainiac.software/api/experimentation/guardrail-check",
      "parameters": {
        "type": "object",
        "properties": {
          "alpha": {
            "default": 0.05,
            "type": "number",
            "exclusiveMinimum": 0,
            "exclusiveMaximum": 0.5
          },
          "metrics": {
            "minItems": 1,
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 64
                },
                "type": {
                  "type": "string",
                  "enum": [
                    "mean",
                    "proportion"
                  ]
                },
                "higherIsBetter": {
                  "default": true,
                  "type": "boolean"
                },
                "marginType": {
                  "type": "string",
                  "enum": [
                    "relative",
                    "absolute"
                  ]
                },
                "margin": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "control": {
                  "anyOf": [
                    {
                      "type": "object",
                      "properties": {
                        "users": {
                          "type": "integer",
                          "minimum": 1,
                          "maximum": 9007199254740991
                        },
                        "conversions": {
                          "type": "integer",
                          "minimum": 0,
                          "maximum": 9007199254740991
                        }
                      },
                      "required": [
                        "users",
                        "conversions"
                      ],
                      "additionalProperties": false
                    },
                    {
                      "type": "object",
                      "properties": {
                        "n": {
                          "type": "integer",
                          "minimum": 2,
                          "maximum": 9007199254740991
                        },
                        "mean": {
                          "type": "number"
                        },
                        "sd": {
                          "type": "number",
                          "minimum": 0
                        }
                      },
                      "required": [
                        "n",
                        "mean",
                        "sd"
                      ],
                      "additionalProperties": false
                    }
                  ]
                },
                "treatment": {
                  "anyOf": [
                    {
                      "type": "object",
                      "properties": {
                        "users": {
                          "type": "integer",
                          "minimum": 1,
                          "maximum": 9007199254740991
                        },
                        "conversions": {
                          "type": "integer",
                          "minimum": 0,
                          "maximum": 9007199254740991
                        }
                      },
                      "required": [
                        "users",
                        "conversions"
                      ],
                      "additionalProperties": false
                    },
                    {
                      "type": "object",
                      "properties": {
                        "n": {
                          "type": "integer",
                          "minimum": 2,
                          "maximum": 9007199254740991
                        },
                        "mean": {
                          "type": "number"
                        },
                        "sd": {
                          "type": "number",
                          "minimum": 0
                        }
                      },
                      "required": [
                        "n",
                        "mean",
                        "sd"
                      ],
                      "additionalProperties": false
                    }
                  ]
                }
              },
              "required": [
                "name",
                "type",
                "marginType",
                "margin",
                "control",
                "treatment"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "metrics"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "experimentation__holdout-impact",
      "description": "Measure cumulative impact against a long-term holdout. Exposed-versus-holdout impact with confidence interval and p-value, plus diluted population-level impact for partial exposure. Docs: https://www.brainiac.software/api/experimentation/holdout-impact",
      "parameters": {
        "type": "object",
        "properties": {
          "metricType": {
            "type": "string",
            "enum": [
              "proportion",
              "mean"
            ]
          },
          "holdout": {
            "anyOf": [
              {
                "type": "object",
                "properties": {
                  "users": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 9007199254740991
                  },
                  "conversions": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 9007199254740991
                  }
                },
                "required": [
                  "users",
                  "conversions"
                ],
                "additionalProperties": false
              },
              {
                "type": "object",
                "properties": {
                  "n": {
                    "type": "integer",
                    "minimum": 2,
                    "maximum": 9007199254740991
                  },
                  "mean": {
                    "type": "number"
                  },
                  "sd": {
                    "type": "number",
                    "minimum": 0
                  }
                },
                "required": [
                  "n",
                  "mean",
                  "sd"
                ],
                "additionalProperties": false
              }
            ]
          },
          "exposed": {
            "anyOf": [
              {
                "type": "object",
                "properties": {
                  "users": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 9007199254740991
                  },
                  "conversions": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 9007199254740991
                  }
                },
                "required": [
                  "users",
                  "conversions"
                ],
                "additionalProperties": false
              },
              {
                "type": "object",
                "properties": {
                  "n": {
                    "type": "integer",
                    "minimum": 2,
                    "maximum": 9007199254740991
                  },
                  "mean": {
                    "type": "number"
                  },
                  "sd": {
                    "type": "number",
                    "minimum": 0
                  }
                },
                "required": [
                  "n",
                  "mean",
                  "sd"
                ],
                "additionalProperties": false
              }
            ]
          },
          "exposureRate": {
            "type": "number",
            "exclusiveMinimum": 0,
            "maximum": 1
          },
          "alpha": {
            "default": 0.05,
            "type": "number",
            "exclusiveMinimum": 0,
            "exclusiveMaximum": 0.5
          }
        },
        "required": [
          "metricType",
          "holdout",
          "exposed"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "experimentation__ab-test-frequentist": "0.02",
  "experimentation__bayesian-ab": "0.03",
  "experimentation__sequential-test": "0.04",
  "experimentation__cuped-adjust": "0.03",
  "experimentation__sample-ratio-mismatch": "0.01",
  "experimentation__sample-size-mde": "0.01",
  "experimentation__multiple-testing-correct": "0.01",
  "experimentation__delta-method-ratio": "0.03",
  "experimentation__bandit-allocate": "0.03",
  "experimentation__bucket-assign": "0.01",
  "experimentation__flag-rule-evaluate": "0.01",
  "experimentation__novelty-effect-detect": "0.01",
  "experimentation__segment-lift": "0.02",
  "experimentation__guardrail-check": "0.02",
  "experimentation__holdout-impact": "0.01"
}
TOOL_ROUTES: Dict[str, str] = {
  "experimentation__ab-test-frequentist": "experimentation/ab-test-frequentist",
  "experimentation__bayesian-ab": "experimentation/bayesian-ab",
  "experimentation__sequential-test": "experimentation/sequential-test",
  "experimentation__cuped-adjust": "experimentation/cuped-adjust",
  "experimentation__sample-ratio-mismatch": "experimentation/sample-ratio-mismatch",
  "experimentation__sample-size-mde": "experimentation/sample-size-mde",
  "experimentation__multiple-testing-correct": "experimentation/multiple-testing-correct",
  "experimentation__delta-method-ratio": "experimentation/delta-method-ratio",
  "experimentation__bandit-allocate": "experimentation/bandit-allocate",
  "experimentation__bucket-assign": "experimentation/bucket-assign",
  "experimentation__flag-rule-evaluate": "experimentation/flag-rule-evaluate",
  "experimentation__novelty-effect-detect": "experimentation/novelty-effect-detect",
  "experimentation__segment-lift": "experimentation/segment-lift",
  "experimentation__guardrail-check": "experimentation/guardrail-check",
  "experimentation__holdout-impact": "experimentation/holdout-impact"
}


class BrainiacExperimentationAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — experimentation",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the experimentation catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "experimentation", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Run a frequentist A/B test scorecard"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.01",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the experimentation group. "
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
