"""Auto-generated BRAINIAC Heurist Mesh agent for group `statistics` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "statistics__t-test",
      "description": "Run a t-test with confidence interval. One-sample, two-sample (Welch or pooled) and paired t-tests with the estimate, statistic, degrees of freedom, p-value, confidence interval and Cohen's d from caller-supplied numbers. Pure computation; no data is stored or fetched. Docs: https://www.brainiac.software/api/statistics/t-test",
      "parameters": {
        "type": "object",
        "properties": {
          "kind": {
            "type": "string",
            "enum": [
              "one_sample",
              "two_sample",
              "paired"
            ]
          },
          "x": {
            "minItems": 2,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "type": [
                "number",
                "null"
              ]
            }
          },
          "y": {
            "maxItems": 100000,
            "type": "array",
            "items": {
              "type": [
                "number",
                "null"
              ]
            }
          },
          "equalVariance": {
            "default": false,
            "type": "boolean"
          },
          "mu0": {
            "default": 0,
            "type": "number"
          },
          "alternative": {
            "default": "two-sided",
            "type": "string",
            "enum": [
              "two-sided",
              "less",
              "greater"
            ]
          },
          "confidence": {
            "default": 0.95,
            "type": "number",
            "exclusiveMinimum": 0.5,
            "exclusiveMaximum": 0.9999
          }
        },
        "required": [
          "kind",
          "x"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "statistics__anova",
      "description": "Run one-way or two-way ANOVA. One-way and two-way ANOVA with interaction (Type II or III sums of squares), R-squared, Tukey HSD post-hoc comparisons and the Brown-Forsythe (median-centred Levene) test of equal variances. Sums of squares use centred two-pass accumulation and match NIST StRD SiRstv. Docs: https://www.brainiac.software/api/statistics/anova",
      "parameters": {
        "type": "object",
        "properties": {
          "design": {
            "type": "string",
            "enum": [
              "one_way",
              "two_way"
            ]
          },
          "rows": {
            "minItems": 3,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "y": {
                  "type": [
                    "number",
                    "null"
                  ]
                },
                "a": {
                  "type": "string",
                  "minLength": 1
                },
                "b": {
                  "type": "string",
                  "minLength": 1
                }
              },
              "required": [
                "y",
                "a"
              ],
              "additionalProperties": false
            }
          },
          "posthoc": {
            "default": "none",
            "type": "string",
            "enum": [
              "tukey",
              "none"
            ]
          },
          "levene": {
            "default": false,
            "type": "boolean"
          },
          "ssType": {
            "default": "II",
            "type": "string",
            "enum": [
              "II",
              "III"
            ]
          },
          "confidence": {
            "default": 0.95,
            "type": "number",
            "exclusiveMinimum": 0.5,
            "exclusiveMaximum": 0.9999
          }
        },
        "required": [
          "design",
          "rows"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "statistics__chi-square-test",
      "description": "Run a chi-square test. Chi-square test of independence (with optional Yates correction), goodness of fit, Fisher's exact test for 2x2 tables and Cramer's V, with expected counts and a low-expected-cell warning. Docs: https://www.brainiac.software/api/statistics/chi-square-test",
      "parameters": {
        "type": "object",
        "properties": {
          "kind": {
            "type": "string",
            "enum": [
              "independence",
              "goodness_of_fit"
            ]
          },
          "table": {
            "minItems": 2,
            "maxItems": 50,
            "type": "array",
            "items": {
              "minItems": 2,
              "maxItems": 50,
              "type": "array",
              "items": {
                "type": "integer",
                "minimum": 0,
                "maximum": 9007199254740991
              }
            }
          },
          "yates": {
            "default": false,
            "type": "boolean"
          },
          "fisher": {
            "default": false,
            "type": "boolean"
          },
          "observed": {
            "minItems": 2,
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "integer",
              "minimum": 0,
              "maximum": 9007199254740991
            }
          },
          "expectedProportions": {
            "minItems": 2,
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "number",
              "minimum": 0
            }
          }
        },
        "required": [
          "kind"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "statistics__nonparametric-tests",
      "description": "Run a nonparametric test. Mann-Whitney U, Wilcoxon signed-rank, Kruskal-Wallis, Friedman and sign tests with average-rank ties, exact p-values for samples up to 50 and tie-corrected normal approximations. Docs: https://www.brainiac.software/api/statistics/nonparametric-tests",
      "parameters": {
        "type": "object",
        "properties": {
          "test": {
            "type": "string",
            "enum": [
              "mann_whitney",
              "wilcoxon_signed_rank",
              "kruskal_wallis",
              "friedman",
              "sign"
            ]
          },
          "x": {
            "minItems": 1,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "type": [
                "number",
                "null"
              ]
            }
          },
          "y": {
            "minItems": 1,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "type": [
                "number",
                "null"
              ]
            }
          },
          "groups": {
            "minItems": 2,
            "maxItems": 100,
            "type": "array",
            "items": {
              "minItems": 1,
              "maxItems": 100000,
              "type": "array",
              "items": {
                "type": [
                  "number",
                  "null"
                ]
              }
            }
          },
          "blocks": {
            "minItems": 2,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "minItems": 2,
              "maxItems": 100,
              "type": "array",
              "items": {
                "type": "number"
              }
            }
          },
          "mu0": {
            "default": 0,
            "type": "number"
          },
          "exact": {
            "default": "auto",
            "anyOf": [
              {
                "type": "string",
                "const": "auto"
              },
              {
                "type": "boolean"
              }
            ]
          }
        },
        "required": [
          "test"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "statistics__linear-regression",
      "description": "Fit a multiple linear regression. Ordinary least squares by Householder QR with coefficient standard errors, t-tests and intervals, R-squared, F, VIF, Durbin-Watson, Breusch-Pagan and confidence and prediction intervals. Matches NIST StRD Norris and Longley. Docs: https://www.brainiac.software/api/statistics/linear-regression",
      "parameters": {
        "type": "object",
        "properties": {
          "y": {
            "minItems": 3,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "type": [
                "number",
                "null"
              ]
            }
          },
          "X": {
            "minItems": 3,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "minItems": 1,
              "maxItems": 50,
              "type": "array",
              "items": {
                "type": [
                  "number",
                  "null"
                ]
              }
            }
          },
          "names": {
            "maxItems": 50,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1
            }
          },
          "intercept": {
            "default": true,
            "type": "boolean"
          },
          "predict": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "minItems": 1,
              "maxItems": 50,
              "type": "array",
              "items": {
                "type": "number"
              }
            }
          },
          "confidence": {
            "default": 0.95,
            "type": "number",
            "exclusiveMinimum": 0.5,
            "exclusiveMaximum": 0.9999
          }
        },
        "required": [
          "y",
          "X"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "statistics__logistic-regression",
      "description": "Fit a binary logistic regression. Binary logistic regression by iteratively reweighted least squares with odds ratios and intervals, deviance, AIC, Hosmer-Lemeshow goodness of fit, a confusion matrix at a chosen threshold and complete-separation detection. Docs: https://www.brainiac.software/api/statistics/logistic-regression",
      "parameters": {
        "type": "object",
        "properties": {
          "y": {
            "minItems": 10,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "anyOf": [
                {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 1
                },
                {
                  "type": "null"
                }
              ]
            }
          },
          "X": {
            "minItems": 10,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "minItems": 1,
              "maxItems": 30,
              "type": "array",
              "items": {
                "type": [
                  "number",
                  "null"
                ]
              }
            }
          },
          "names": {
            "maxItems": 30,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1
            }
          },
          "threshold": {
            "default": 0.5,
            "type": "number",
            "exclusiveMinimum": 0,
            "exclusiveMaximum": 1
          },
          "hlGroups": {
            "default": 10,
            "type": "integer",
            "minimum": 3,
            "maximum": 50
          }
        },
        "required": [
          "y",
          "X"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "statistics__normality-test",
      "description": "Test data for normality. Anderson-Darling, Shapiro-Wilk (Royston AS R94) and Lilliefors tests of normality with optional normal probability plot coordinates. Shapiro-Wilk and Anderson-Darling agree with SciPy and statsmodels. Docs: https://www.brainiac.software/api/statistics/normality-test",
      "parameters": {
        "type": "object",
        "properties": {
          "x": {
            "minItems": 3,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "type": [
                "number",
                "null"
              ]
            }
          },
          "tests": {
            "default": [
              "anderson_darling",
              "shapiro_wilk",
              "lilliefors"
            ],
            "minItems": 1,
            "maxItems": 3,
            "type": "array",
            "items": {
              "type": "string",
              "enum": [
                "anderson_darling",
                "shapiro_wilk",
                "lilliefors"
              ]
            }
          },
          "plot": {
            "default": false,
            "type": "boolean"
          }
        },
        "required": [
          "x"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "statistics__power-sample-size",
      "description": "Calculate statistical power or sample size. Power or required sample size for a two-sample t-test (noncentral t), one-way ANOVA (noncentral F), two proportions (Cohen's h) and a correlation (Fisher z). Exactly one of n or power is solved. Docs: https://www.brainiac.software/api/statistics/power-sample-size",
      "parameters": {
        "type": "object",
        "properties": {
          "test": {
            "type": "string",
            "enum": [
              "t_two_sample",
              "anova_oneway",
              "two_proportions",
              "correlation"
            ]
          },
          "effectSize": {
            "anyOf": [
              {
                "type": "number",
                "exclusiveMinimum": 0
              },
              {
                "type": "null"
              }
            ]
          },
          "alpha": {
            "default": 0.05,
            "type": "number",
            "exclusiveMinimum": 0,
            "exclusiveMaximum": 1
          },
          "power": {
            "anyOf": [
              {
                "type": "number",
                "exclusiveMinimum": 0,
                "exclusiveMaximum": 1
              },
              {
                "type": "null"
              }
            ]
          },
          "n": {
            "anyOf": [
              {
                "type": "number",
                "exclusiveMinimum": 1,
                "maximum": 10000000
              },
              {
                "type": "null"
              }
            ]
          },
          "groups": {
            "type": "integer",
            "minimum": 2,
            "maximum": 100
          },
          "p1": {
            "anyOf": [
              {
                "type": "number",
                "exclusiveMinimum": 0,
                "exclusiveMaximum": 1
              },
              {
                "type": "null"
              }
            ]
          },
          "p2": {
            "anyOf": [
              {
                "type": "number",
                "exclusiveMinimum": 0,
                "exclusiveMaximum": 1
              },
              {
                "type": "null"
              }
            ]
          },
          "r": {
            "anyOf": [
              {
                "type": "number",
                "exclusiveMinimum": -1,
                "exclusiveMaximum": 1
              },
              {
                "type": "null"
              }
            ]
          }
        },
        "required": [
          "test"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "statistics__control-chart",
      "description": "Compute control chart limits and violations. Control limits and Western Electric or Nelson rule violations for I-MR, X-bar R, X-bar S, p, np, c and u charts from caller-supplied measurements or counts, with optional fixed Phase II limits. Docs: https://www.brainiac.software/api/statistics/control-chart",
      "parameters": {
        "type": "object",
        "properties": {
          "chart": {
            "type": "string",
            "enum": [
              "imr",
              "xbar_r",
              "xbar_s",
              "p",
              "np",
              "c",
              "u"
            ]
          },
          "values": {
            "minItems": 2,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "type": "number"
            }
          },
          "subgroups": {
            "minItems": 2,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "minItems": 2,
              "maxItems": 50,
              "type": "array",
              "items": {
                "type": "number"
              }
            }
          },
          "counts": {
            "minItems": 2,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "type": "integer",
              "minimum": 0,
              "maximum": 9007199254740991
            }
          },
          "sizes": {
            "minItems": 2,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "type": "integer",
              "minimum": 1,
              "maximum": 9007199254740991
            }
          },
          "size": {
            "type": "integer",
            "minimum": 1,
            "maximum": 9007199254740991
          },
          "rules": {
            "default": [
              "we1"
            ],
            "minItems": 1,
            "maxItems": 8,
            "type": "array",
            "items": {
              "type": "string",
              "enum": [
                "we1",
                "we2",
                "we3",
                "we4",
                "n5",
                "n6",
                "n7",
                "n8"
              ]
            }
          },
          "phase": {
            "default": "I",
            "type": "string",
            "enum": [
              "I",
              "II"
            ]
          },
          "limits": {
            "type": "object",
            "properties": {
              "center": {
                "type": "number"
              },
              "ucl": {
                "type": "number"
              },
              "lcl": {
                "type": "number"
              },
              "secondary": {
                "type": "object",
                "properties": {
                  "center": {
                    "type": "number"
                  },
                  "ucl": {
                    "type": "number"
                  },
                  "lcl": {
                    "type": "number"
                  }
                },
                "required": [
                  "center",
                  "ucl",
                  "lcl"
                ],
                "additionalProperties": false
              }
            },
            "required": [
              "center",
              "ucl",
              "lcl"
            ],
            "additionalProperties": false
          }
        },
        "required": [
          "chart"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "statistics__process-capability",
      "description": "Calculate process capability indices. Cp, Cpk, Pp, Ppk, Cpm and expected parts per million out of specification from individual values or subgroups, with R-bar, S-bar or pooled within-subgroup sigma, an optional Box-Cox transform and a Bissell interval for Cpk. Docs: https://www.brainiac.software/api/statistics/process-capability",
      "parameters": {
        "type": "object",
        "properties": {
          "values": {
            "minItems": 2,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "type": [
                "number",
                "null"
              ]
            }
          },
          "subgroups": {
            "minItems": 2,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "minItems": 2,
              "maxItems": 50,
              "type": "array",
              "items": {
                "type": "number"
              }
            }
          },
          "lsl": {
            "type": "number"
          },
          "usl": {
            "type": "number"
          },
          "target": {
            "type": "number"
          },
          "withinMethod": {
            "default": "rbar",
            "type": "string",
            "enum": [
              "rbar",
              "sbar",
              "pooled"
            ]
          },
          "transform": {
            "default": "none",
            "type": "string",
            "enum": [
              "none",
              "box_cox"
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
      "name": "statistics__gage-rr",
      "description": "Run a crossed gage R&R study. Crossed gage repeatability and reproducibility by the ANOVA method: variance components, percent contribution, percent study variation, percent tolerance and number of distinct categories for a balanced parts by operators by replicates study. Docs: https://www.brainiac.software/api/statistics/gage-rr",
      "parameters": {
        "type": "object",
        "properties": {
          "measurements": {
            "minItems": 8,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "part": {
                  "type": "string",
                  "minLength": 1
                },
                "operator": {
                  "type": "string",
                  "minLength": 1
                },
                "value": {
                  "type": "number"
                }
              },
              "required": [
                "part",
                "operator",
                "value"
              ],
              "additionalProperties": false
            }
          },
          "tolerance": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "studyVarMultiplier": {
            "default": 6,
            "anyOf": [
              {
                "type": "number",
                "const": 5.15
              },
              {
                "type": "number",
                "const": 6
              }
            ]
          },
          "removeInteractionAbove": {
            "default": 0.25,
            "type": "number",
            "minimum": 0,
            "maximum": 1
          }
        },
        "required": [
          "measurements"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "statistics__doe-design-generate",
      "description": "Generate a designed experiment. Full and fractional factorial (with defining relation, resolution and alias structure), Plackett-Burman and central composite designs in standard order, optionally randomised with a seeded xorshift128+ shuffle that is reproducible across languages. Docs: https://www.brainiac.software/api/statistics/doe-design-generate",
      "parameters": {
        "type": "object",
        "properties": {
          "type": {
            "type": "string",
            "enum": [
              "full_factorial",
              "fractional_factorial",
              "plackett_burman",
              "central_composite"
            ]
          },
          "factors": {
            "minItems": 2,
            "maxItems": 47,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1
            }
          },
          "generators": {
            "maxItems": 14,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 3
            }
          },
          "centerPoints": {
            "default": 0,
            "type": "integer",
            "minimum": 0,
            "maximum": 1000
          },
          "replicates": {
            "default": 1,
            "type": "integer",
            "minimum": 1,
            "maximum": 100
          },
          "randomize": {
            "default": false,
            "type": "boolean"
          },
          "seed": {
            "default": 1,
            "type": "integer",
            "minimum": -9007199254740991,
            "maximum": 9007199254740991
          },
          "alpha": {
            "default": "rotatable",
            "anyOf": [
              {
                "type": "string",
                "enum": [
                  "rotatable",
                  "face_centered"
                ]
              },
              {
                "type": "number",
                "exclusiveMinimum": 0
              }
            ]
          }
        },
        "required": [
          "type",
          "factors"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "statistics__doe-effects-analyze",
      "description": "Analyse two-level factorial effects. Effects, coefficients and standardised effects for a two-level factorial, with Lenth's pseudo standard error and margin of error for unreplicated designs or a pure-error ANOVA when runs are replicated, sorted as a Pareto of effects. Docs: https://www.brainiac.software/api/statistics/doe-effects-analyze",
      "parameters": {
        "type": "object",
        "properties": {
          "matrix": {
            "minItems": 4,
            "maxItems": 1024,
            "type": "array",
            "items": {
              "type": "object",
              "propertyNames": {
                "type": "string"
              },
              "additionalProperties": {
                "type": "number"
              }
            }
          },
          "response": {
            "minItems": 4,
            "maxItems": 1024,
            "type": "array",
            "items": {
              "type": "number"
            }
          },
          "terms": {
            "default": "all_interactions",
            "type": "string",
            "enum": [
              "main",
              "two_way",
              "all_interactions"
            ]
          },
          "alpha": {
            "default": 0.05,
            "type": "number",
            "exclusiveMinimum": 0,
            "exclusiveMaximum": 1
          }
        },
        "required": [
          "matrix",
          "response"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "statistics__weibull-reliability",
      "description": "Fit a life distribution to censored data. Maximum-likelihood Weibull, lognormal or exponential life fits to right-censored failure data with Fisher-matrix confidence bounds, B-lives, reliability at chosen times and mean time to failure. Docs: https://www.brainiac.software/api/statistics/weibull-reliability",
      "parameters": {
        "type": "object",
        "properties": {
          "times": {
            "minItems": 3,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "type": "number",
              "exclusiveMinimum": 0
            }
          },
          "failed": {
            "minItems": 3,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "type": "integer",
              "minimum": 0,
              "maximum": 1
            }
          },
          "distribution": {
            "default": "weibull",
            "type": "string",
            "enum": [
              "weibull",
              "lognormal",
              "exponential"
            ]
          },
          "bLives": {
            "default": [],
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "number",
              "exclusiveMinimum": 0,
              "exclusiveMaximum": 100
            }
          },
          "reliabilityAt": {
            "default": [],
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "number",
              "exclusiveMinimum": 0
            }
          },
          "confidence": {
            "default": 0.95,
            "type": "number",
            "exclusiveMinimum": 0.5,
            "exclusiveMaximum": 0.9999
          }
        },
        "required": [
          "times",
          "failed"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "statistics__time-series-decompose",
      "description": "Decompose a seasonal time series. Classical moving-average additive or multiplicative decomposition into trend, seasonal indices and remainder, with Wang-Smith-Hyndman strength of seasonality and trend measures. STL is not provided. Docs: https://www.brainiac.software/api/statistics/time-series-decompose",
      "parameters": {
        "type": "object",
        "properties": {
          "values": {
            "minItems": 4,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "type": "number"
            }
          },
          "period": {
            "type": "integer",
            "minimum": 2,
            "maximum": 366
          },
          "model": {
            "default": "additive",
            "type": "string",
            "enum": [
              "additive",
              "multiplicative"
            ]
          }
        },
        "required": [
          "values",
          "period"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "statistics__t-test": "0.02",
  "statistics__anova": "0.03",
  "statistics__chi-square-test": "0.02",
  "statistics__nonparametric-tests": "0.03",
  "statistics__linear-regression": "0.05",
  "statistics__logistic-regression": "0.05",
  "statistics__normality-test": "0.03",
  "statistics__power-sample-size": "0.02",
  "statistics__control-chart": "0.04",
  "statistics__process-capability": "0.04",
  "statistics__gage-rr": "0.05",
  "statistics__doe-design-generate": "0.03",
  "statistics__doe-effects-analyze": "0.03",
  "statistics__weibull-reliability": "0.05",
  "statistics__time-series-decompose": "0.03"
}
TOOL_ROUTES: Dict[str, str] = {
  "statistics__t-test": "statistics/t-test",
  "statistics__anova": "statistics/anova",
  "statistics__chi-square-test": "statistics/chi-square-test",
  "statistics__nonparametric-tests": "statistics/nonparametric-tests",
  "statistics__linear-regression": "statistics/linear-regression",
  "statistics__logistic-regression": "statistics/logistic-regression",
  "statistics__normality-test": "statistics/normality-test",
  "statistics__power-sample-size": "statistics/power-sample-size",
  "statistics__control-chart": "statistics/control-chart",
  "statistics__process-capability": "statistics/process-capability",
  "statistics__gage-rr": "statistics/gage-rr",
  "statistics__doe-design-generate": "statistics/doe-design-generate",
  "statistics__doe-effects-analyze": "statistics/doe-effects-analyze",
  "statistics__weibull-reliability": "statistics/weibull-reliability",
  "statistics__time-series-decompose": "statistics/time-series-decompose"
}


class BrainiacStatisticsAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — statistics",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the statistics catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "statistics", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Run a t-test with confidence interval"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.02",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the statistics group. "
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
