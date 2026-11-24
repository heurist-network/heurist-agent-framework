"""Auto-generated BRAINIAC Heurist Mesh agent for group `predictive-analytics` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "predictive-analytics__kmeans-cluster",
      "description": "K-means clustering with silhouette k-selection. Lloyd k-means with k-means++ seeding, optional standardisation, nInit restarts, silhouette and inertia for a k range, and stable label renumbering. Docs: https://www.brainiac.software/api/predictive-analytics/kmeans-cluster",
      "parameters": {
        "type": "object",
        "properties": {
          "columns": {
            "minItems": 1,
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 64
            }
          },
          "rows": {
            "minItems": 1,
            "maxItems": 50000,
            "type": "array",
            "items": {
              "type": "array",
              "items": {
                "type": [
                  "number",
                  "null"
                ]
              }
            }
          },
          "k": {
            "type": "integer",
            "minimum": 2,
            "maximum": 50
          },
          "kRange": {
            "type": "array",
            "prefixItems": [
              {
                "type": "integer",
                "minimum": 2,
                "maximum": 9007199254740991
              },
              {
                "type": "integer",
                "minimum": -9007199254740991,
                "maximum": 50
              }
            ],
            "items": false,
            "minItems": 2,
            "maxItems": 2
          },
          "standardize": {
            "default": true,
            "type": "boolean"
          },
          "seed": {
            "default": 42,
            "type": "integer",
            "minimum": -9007199254740991,
            "maximum": 9007199254740991
          },
          "nInit": {
            "default": 10,
            "type": "integer",
            "minimum": 1,
            "maximum": 50
          },
          "maxIter": {
            "default": 300,
            "type": "integer",
            "minimum": 1,
            "maximum": 1000
          }
        },
        "required": [
          "columns",
          "rows"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "predictive-analytics__dbscan-cluster",
      "description": "DBSCAN density clustering with noise labels. Density-based clustering with Euclidean or haversine distance, core/border/noise labelling, and an optional k-distance knee suggestion for eps. Docs: https://www.brainiac.software/api/predictive-analytics/dbscan-cluster",
      "parameters": {
        "type": "object",
        "properties": {
          "columns": {
            "minItems": 1,
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 64
            }
          },
          "rows": {
            "minItems": 1,
            "maxItems": 50000,
            "type": "array",
            "items": {
              "type": "array",
              "items": {
                "type": [
                  "number",
                  "null"
                ]
              }
            }
          },
          "eps": {
            "type": "number",
            "exclusiveMinimum": 0
          },
          "minSamples": {
            "default": 5,
            "type": "integer",
            "minimum": 2,
            "maximum": 1000
          },
          "metric": {
            "default": "euclidean",
            "type": "string",
            "enum": [
              "euclidean",
              "haversine"
            ]
          },
          "kDistance": {
            "default": false,
            "type": "boolean"
          }
        },
        "required": [
          "columns",
          "rows",
          "eps"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "predictive-analytics__pca",
      "description": "Principal component analysis. Centre (and optionally standardise) columns, decompose the covariance, and return eigenvalues, explained ratios, signed loadings and optional scores. Docs: https://www.brainiac.software/api/predictive-analytics/pca",
      "parameters": {
        "type": "object",
        "properties": {
          "columns": {
            "minItems": 1,
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 64
            }
          },
          "rows": {
            "minItems": 1,
            "maxItems": 50000,
            "type": "array",
            "items": {
              "type": "array",
              "items": {
                "type": [
                  "number",
                  "null"
                ]
              }
            }
          },
          "standardize": {
            "default": false,
            "type": "boolean"
          },
          "components": {
            "type": "integer",
            "minimum": 1,
            "maximum": 100
          },
          "returnScores": {
            "default": true,
            "type": "boolean"
          }
        },
        "required": [
          "columns",
          "rows"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "predictive-analytics__decision-tree-train",
      "description": "Train a CART decision tree. Fit a classification or regression CART tree with depth and leaf limits, readable rules, feature importance and optional predictions. Docs: https://www.brainiac.software/api/predictive-analytics/decision-tree-train",
      "parameters": {
        "type": "object",
        "properties": {
          "task": {
            "type": "string",
            "enum": [
              "classification",
              "regression"
            ]
          },
          "columns": {
            "minItems": 1,
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 64
            }
          },
          "rows": {
            "minItems": 2,
            "maxItems": 50000,
            "type": "array",
            "items": {
              "type": "array",
              "items": {
                "type": [
                  "number",
                  "null"
                ]
              }
            }
          },
          "target": {
            "minItems": 2,
            "maxItems": 50000,
            "type": "array",
            "items": {
              "anyOf": [
                {
                  "type": "number"
                },
                {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 64
                }
              ]
            }
          },
          "maxDepth": {
            "default": 5,
            "type": "integer",
            "minimum": 1,
            "maximum": 20
          },
          "minSamplesLeaf": {
            "default": 1,
            "type": "integer",
            "minimum": 1,
            "maximum": 1000
          },
          "predict": {
            "maxItems": 10000,
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
          "task",
          "columns",
          "rows",
          "target"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "predictive-analytics__random-forest-importance",
      "description": "Random-forest OOB score and permutation importance. Train a small seeded random forest, report out-of-bag accuracy or R², and estimate permutation feature importance with Fisher-Yates shuffles. Docs: https://www.brainiac.software/api/predictive-analytics/random-forest-importance",
      "parameters": {
        "type": "object",
        "properties": {
          "task": {
            "type": "string",
            "enum": [
              "classification",
              "regression"
            ]
          },
          "columns": {
            "minItems": 1,
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 64
            }
          },
          "rows": {
            "minItems": 2,
            "maxItems": 50000,
            "type": "array",
            "items": {
              "type": "array",
              "items": {
                "type": [
                  "number",
                  "null"
                ]
              }
            }
          },
          "target": {
            "minItems": 2,
            "maxItems": 50000,
            "type": "array",
            "items": {
              "anyOf": [
                {
                  "type": "number"
                },
                {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 64
                }
              ]
            }
          },
          "trees": {
            "default": 100,
            "type": "integer",
            "minimum": 10,
            "maximum": 500
          },
          "maxFeatures": {
            "default": "sqrt",
            "anyOf": [
              {
                "type": "string",
                "enum": [
                  "sqrt",
                  "log2"
                ]
              },
              {
                "type": "integer",
                "minimum": 1,
                "maximum": 100
              }
            ]
          },
          "maxDepth": {
            "default": null,
            "anyOf": [
              {
                "type": "integer",
                "minimum": 1,
                "maximum": 20
              },
              {
                "type": "null"
              }
            ]
          },
          "seed": {
            "default": 42,
            "type": "integer",
            "minimum": -9007199254740991,
            "maximum": 9007199254740991
          },
          "permutationRepeats": {
            "default": 5,
            "type": "integer",
            "minimum": 1,
            "maximum": 50
          },
          "minSamplesLeaf": {
            "default": 1,
            "type": "integer",
            "minimum": 1,
            "maximum": 1000
          }
        },
        "required": [
          "task",
          "columns",
          "rows",
          "target"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "predictive-analytics__kaplan-meier-survival",
      "description": "Kaplan-Meier survival curves and log-rank test. Estimate group Kaplan-Meier curves with Greenwood log-log confidence intervals, median survival, survival at chosen times, and a multi-group log-rank test. Docs: https://www.brainiac.software/api/predictive-analytics/kaplan-meier-survival",
      "parameters": {
        "type": "object",
        "properties": {
          "subjects": {
            "minItems": 2,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "time": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "event": {
                  "anyOf": [
                    {
                      "type": "number",
                      "const": 0
                    },
                    {
                      "type": "number",
                      "const": 1
                    }
                  ]
                },
                "group": {
                  "default": "all",
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 64
                }
              },
              "required": [
                "time",
                "event"
              ],
              "additionalProperties": false
            }
          },
          "confidence": {
            "default": 0.95,
            "type": "number",
            "exclusiveMinimum": 0,
            "exclusiveMaximum": 1
          },
          "at": {
            "maxItems": 1000,
            "type": "array",
            "items": {
              "type": "number",
              "exclusiveMinimum": 0
            }
          }
        },
        "required": [
          "subjects"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "predictive-analytics__cox-regression",
      "description": "Cox proportional hazards regression. Maximise the Cox partial likelihood with Efron or Breslow ties, return hazard ratios with SEs, concordance, and a rank-time proportional-hazards check. Docs: https://www.brainiac.software/api/predictive-analytics/cox-regression",
      "parameters": {
        "type": "object",
        "properties": {
          "subjects": {
            "minItems": 2,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "time": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "event": {
                  "anyOf": [
                    {
                      "type": "number",
                      "const": 0
                    },
                    {
                      "type": "number",
                      "const": 1
                    }
                  ]
                },
                "covariates": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 64
                  },
                  "additionalProperties": {
                    "type": "number"
                  }
                }
              },
              "required": [
                "time",
                "event",
                "covariates"
              ],
              "additionalProperties": false
            }
          },
          "ties": {
            "default": "efron",
            "type": "string",
            "enum": [
              "efron",
              "breslow"
            ]
          },
          "confidence": {
            "default": 0.95,
            "type": "number",
            "exclusiveMinimum": 0,
            "exclusiveMaximum": 1
          }
        },
        "required": [
          "subjects"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "predictive-analytics__cohort-retention",
      "description": "Cohort retention matrix and weighted curve. Build day/week/month cohort retention in classic or rolling mode from signup and activity dates, with partial-period flags and a size-weighted curve. Docs: https://www.brainiac.software/api/predictive-analytics/cohort-retention",
      "parameters": {
        "type": "object",
        "properties": {
          "events": {
            "minItems": 1,
            "maxItems": 200000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "userId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 128
                },
                "signup": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                },
                "activity": {
                  "minItems": 1,
                  "maxItems": 10000,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                  }
                }
              },
              "required": [
                "userId",
                "signup",
                "activity"
              ],
              "additionalProperties": false
            }
          },
          "period": {
            "default": "month",
            "type": "string",
            "enum": [
              "day",
              "week",
              "month"
            ]
          },
          "mode": {
            "default": "classic",
            "type": "string",
            "enum": [
              "classic",
              "rolling"
            ]
          },
          "asOf": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
          },
          "timezone": {
            "default": "UTC",
            "type": "string",
            "minLength": 1,
            "maxLength": 64
          }
        },
        "required": [
          "events",
          "asOf"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "predictive-analytics__rfm-segment",
      "description": "RFM scoring and named customer segments. Score customers 1–bins on recency, frequency and monetary value with average ranks for ties, then map scores to Champions/Loyal/New/At risk/Hibernating or a custom rule list. Docs: https://www.brainiac.software/api/predictive-analytics/rfm-segment",
      "parameters": {
        "type": "object",
        "properties": {
          "customers": {
            "minItems": 1,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 128
                },
                "recencyDays": {
                  "type": "number",
                  "minimum": 0
                },
                "frequency": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "monetary": {
                  "type": "number",
                  "minimum": 0
                }
              },
              "required": [
                "id",
                "recencyDays",
                "frequency",
                "monetary"
              ],
              "additionalProperties": false
            }
          },
          "transactions": {
            "minItems": 1,
            "maxItems": 1000000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "customerId": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 128
                },
                "date": {
                  "type": "string",
                  "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
                },
                "amount": {
                  "type": "number"
                }
              },
              "required": [
                "customerId",
                "date",
                "amount"
              ],
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "pattern": "^\\d{4}-\\d{2}-\\d{2}$"
          },
          "bins": {
            "default": 5,
            "type": "integer",
            "minimum": 3,
            "maximum": 10
          },
          "segmentMap": {
            "default": "default",
            "anyOf": [
              {
                "type": "string",
                "const": "default"
              },
              {
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
                    "r": {
                      "type": "array",
                      "prefixItems": [
                        {
                          "type": "integer",
                          "minimum": 1,
                          "maximum": 9007199254740991
                        },
                        {
                          "type": "integer",
                          "minimum": -9007199254740991,
                          "maximum": 10
                        }
                      ],
                      "items": false,
                      "minItems": 2,
                      "maxItems": 2
                    },
                    "f": {
                      "type": "array",
                      "prefixItems": [
                        {
                          "type": "integer",
                          "minimum": 1,
                          "maximum": 9007199254740991
                        },
                        {
                          "type": "integer",
                          "minimum": -9007199254740991,
                          "maximum": 10
                        }
                      ],
                      "items": false,
                      "minItems": 2,
                      "maxItems": 2
                    },
                    "m": {
                      "type": "array",
                      "prefixItems": [
                        {
                          "type": "integer",
                          "minimum": 1,
                          "maximum": 9007199254740991
                        },
                        {
                          "type": "integer",
                          "minimum": -9007199254740991,
                          "maximum": 10
                        }
                      ],
                      "items": false,
                      "minItems": 2,
                      "maxItems": 2
                    }
                  },
                  "required": [
                    "name",
                    "r",
                    "f"
                  ],
                  "additionalProperties": false
                }
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
      "name": "predictive-analytics__clv-bg-nbd",
      "description": "BG/NBD and Gamma-Gamma customer lifetime value. Fit BG/NBD purchase frequency and Gamma-Gamma spend models, then return P(alive), expected purchases over a horizon, expected value and undiscounted CLV per customer. Docs: https://www.brainiac.software/api/predictive-analytics/clv-bg-nbd",
      "parameters": {
        "type": "object",
        "properties": {
          "customers": {
            "minItems": 20,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 128
                },
                "frequency": {
                  "type": "integer",
                  "minimum": 0,
                  "maximum": 9007199254740991
                },
                "recency": {
                  "type": "number",
                  "minimum": 0
                },
                "T": {
                  "type": "number",
                  "exclusiveMinimum": 0
                },
                "monetaryValue": {
                  "type": "number",
                  "exclusiveMinimum": 0
                }
              },
              "required": [
                "id",
                "frequency",
                "recency",
                "T"
              ],
              "additionalProperties": false
            }
          },
          "horizon": {
            "default": 10,
            "type": "number",
            "exclusiveMinimum": 0
          },
          "margin": {
            "default": 1,
            "type": "number",
            "exclusiveMinimum": 0
          },
          "minRepeatCustomers": {
            "default": 10,
            "type": "integer",
            "minimum": 1,
            "maximum": 100000
          }
        },
        "required": [
          "customers"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "predictive-analytics__market-basket-rules",
      "description": "Market-basket association rules. Mine frequent itemsets and association rules with support, confidence, lift, leverage and conviction from caller baskets. Docs: https://www.brainiac.software/api/predictive-analytics/market-basket-rules",
      "parameters": {
        "type": "object",
        "properties": {
          "baskets": {
            "minItems": 1,
            "maxItems": 200000,
            "type": "array",
            "items": {
              "minItems": 1,
              "maxItems": 200,
              "type": "array",
              "items": {
                "type": "string",
                "minLength": 1,
                "maxLength": 128
              }
            }
          },
          "minSupport": {
            "default": 0.01,
            "type": "number",
            "exclusiveMinimum": 0,
            "maximum": 1
          },
          "minConfidence": {
            "default": 0.5,
            "type": "number",
            "exclusiveMinimum": 0,
            "maximum": 1
          },
          "maxItemsetSize": {
            "default": 3,
            "type": "integer",
            "minimum": 2,
            "maximum": 10
          },
          "maxRules": {
            "default": 1000,
            "type": "integer",
            "minimum": 1,
            "maximum": 100000
          }
        },
        "required": [
          "baskets"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "predictive-analytics__changepoint-detect",
      "description": "PELT changepoint detection. Detect mean or mean-variance changepoints with PELT, BIC/AIC or custom penalties, and MAD-based noise scaling. Docs: https://www.brainiac.software/api/predictive-analytics/changepoint-detect",
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
          "model": {
            "default": "mean",
            "type": "string",
            "enum": [
              "mean",
              "meanvar"
            ]
          },
          "penalty": {
            "default": "bic",
            "anyOf": [
              {
                "type": "string",
                "enum": [
                  "bic",
                  "aic"
                ]
              },
              {
                "type": "number",
                "exclusiveMinimum": 0
              }
            ]
          },
          "minSegment": {
            "default": 2,
            "type": "integer",
            "minimum": 1,
            "maximum": 10000
          }
        },
        "required": [
          "values"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "predictive-analytics__classification-metrics",
      "description": "ROC, PR, Brier and calibration metrics. Compute ROC-AUC, average precision, Brier score, confusion at a threshold, Youden-optimal threshold and equal-width calibration bins from binary labels and scores. Docs: https://www.brainiac.software/api/predictive-analytics/classification-metrics",
      "parameters": {
        "type": "object",
        "properties": {
          "labels": {
            "minItems": 2,
            "maxItems": 1000000,
            "type": "array",
            "items": {
              "anyOf": [
                {
                  "type": "number",
                  "const": 0
                },
                {
                  "type": "number",
                  "const": 1
                }
              ]
            }
          },
          "scores": {
            "minItems": 2,
            "maxItems": 1000000,
            "type": "array",
            "items": {
              "type": "number"
            }
          },
          "threshold": {
            "default": 0.5,
            "type": "number",
            "minimum": 0,
            "maximum": 1
          },
          "calibrationBins": {
            "default": 10,
            "type": "integer",
            "minimum": 2,
            "maximum": 100
          }
        },
        "required": [
          "labels",
          "scores"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "predictive-analytics__correlation-analysis",
      "description": "Pearson, Spearman, Kendall and partial correlations. Pairwise Pearson/Spearman/Kendall correlations with p-values, optional partial correlations, and Holm/BH/Bonferroni adjustment across pair-method tests. Docs: https://www.brainiac.software/api/predictive-analytics/correlation-analysis",
      "parameters": {
        "type": "object",
        "properties": {
          "columns": {
            "minItems": 1,
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 64
            }
          },
          "rows": {
            "minItems": 1,
            "maxItems": 50000,
            "type": "array",
            "items": {
              "type": "array",
              "items": {
                "type": [
                  "number",
                  "null"
                ]
              }
            }
          },
          "methods": {
            "default": [
              "pearson"
            ],
            "minItems": 1,
            "maxItems": 3,
            "type": "array",
            "items": {
              "type": "string",
              "enum": [
                "pearson",
                "spearman",
                "kendall"
              ]
            }
          },
          "partial": {
            "maxItems": 100,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "x": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 64
                },
                "y": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 64
                },
                "given": {
                  "default": [],
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 64
                  }
                }
              },
              "required": [
                "x",
                "y"
              ],
              "additionalProperties": false
            }
          },
          "adjust": {
            "default": "none",
            "type": "string",
            "enum": [
              "none",
              "holm",
              "bh",
              "bonferroni"
            ]
          }
        },
        "required": [
          "columns",
          "rows"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "predictive-analytics__propensity-score-match",
      "description": "Propensity-score matching with balance diagnostics. Fit logistic propensity scores, match treated to controls 1:1 on the logit within a caliper, and report SMD balance and common-support counts. Docs: https://www.brainiac.software/api/predictive-analytics/propensity-score-match",
      "parameters": {
        "type": "object",
        "properties": {
          "units": {
            "minItems": 10,
            "maxItems": 100000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 128
                },
                "treated": {
                  "anyOf": [
                    {
                      "type": "number",
                      "const": 0
                    },
                    {
                      "type": "number",
                      "const": 1
                    }
                  ]
                },
                "covariates": {
                  "type": "object",
                  "propertyNames": {
                    "type": "string",
                    "minLength": 1,
                    "maxLength": 64
                  },
                  "additionalProperties": {
                    "type": "number"
                  }
                }
              },
              "required": [
                "id",
                "treated",
                "covariates"
              ],
              "additionalProperties": false
            }
          },
          "caliperSdLogit": {
            "default": 0.2,
            "type": "number",
            "exclusiveMinimum": 0
          },
          "replacement": {
            "default": false,
            "type": "boolean"
          },
          "order": {
            "default": "descending_score",
            "type": "string",
            "enum": [
              "descending_score",
              "ascending_score",
              "random"
            ]
          },
          "seed": {
            "default": 42,
            "type": "integer",
            "minimum": -9007199254740991,
            "maximum": 9007199254740991
          }
        },
        "required": [
          "units"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "predictive-analytics__kmeans-cluster": "0.04",
  "predictive-analytics__dbscan-cluster": "0.04",
  "predictive-analytics__pca": "0.03",
  "predictive-analytics__decision-tree-train": "0.03",
  "predictive-analytics__random-forest-importance": "0.05",
  "predictive-analytics__kaplan-meier-survival": "0.04",
  "predictive-analytics__cox-regression": "0.05",
  "predictive-analytics__cohort-retention": "0.03",
  "predictive-analytics__rfm-segment": "0.03",
  "predictive-analytics__clv-bg-nbd": "0.05",
  "predictive-analytics__market-basket-rules": "0.04",
  "predictive-analytics__changepoint-detect": "0.03",
  "predictive-analytics__classification-metrics": "0.02",
  "predictive-analytics__correlation-analysis": "0.03",
  "predictive-analytics__propensity-score-match": "0.04"
}
TOOL_ROUTES: Dict[str, str] = {
  "predictive-analytics__kmeans-cluster": "predictive-analytics/kmeans-cluster",
  "predictive-analytics__dbscan-cluster": "predictive-analytics/dbscan-cluster",
  "predictive-analytics__pca": "predictive-analytics/pca",
  "predictive-analytics__decision-tree-train": "predictive-analytics/decision-tree-train",
  "predictive-analytics__random-forest-importance": "predictive-analytics/random-forest-importance",
  "predictive-analytics__kaplan-meier-survival": "predictive-analytics/kaplan-meier-survival",
  "predictive-analytics__cox-regression": "predictive-analytics/cox-regression",
  "predictive-analytics__cohort-retention": "predictive-analytics/cohort-retention",
  "predictive-analytics__rfm-segment": "predictive-analytics/rfm-segment",
  "predictive-analytics__clv-bg-nbd": "predictive-analytics/clv-bg-nbd",
  "predictive-analytics__market-basket-rules": "predictive-analytics/market-basket-rules",
  "predictive-analytics__changepoint-detect": "predictive-analytics/changepoint-detect",
  "predictive-analytics__classification-metrics": "predictive-analytics/classification-metrics",
  "predictive-analytics__correlation-analysis": "predictive-analytics/correlation-analysis",
  "predictive-analytics__propensity-score-match": "predictive-analytics/propensity-score-match"
}


class BrainiacPredictiveAnalyticsAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — predictive-analytics",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the predictive-analytics catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "predictive-analytics", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["K-means clustering with silhouette k-selection"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.02",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the predictive-analytics group. "
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
