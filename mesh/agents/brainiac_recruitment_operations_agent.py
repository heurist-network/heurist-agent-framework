"""Auto-generated BRAINIAC Heurist Mesh agent for group `recruitment-operations` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "recruitment-operations__job-description-structure",
      "description": "Structure a job description. Read Title, Requirement, and Responsibility lines into explicit requirements. Unlabeled prose is not turned into a requirement, and a requirement counts toward a score only when it is marked required. Docs: https://www.brainiac.software/api/recruitment-operations/job-description-structure",
      "parameters": {
        "type": "object",
        "properties": {
          "title": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200
          },
          "jobText": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
          },
          "requirements": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "enum": [
                    "skill",
                    "qualification",
                    "experience",
                    "responsibility"
                  ]
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "minimumYears": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 80
                },
                "strength": {
                  "type": "string",
                  "enum": [
                    "required",
                    "preferred"
                  ]
                }
              },
              "required": [
                "kind",
                "name"
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
      "name": "recruitment-operations__resume-data-extract",
      "description": "Extract resume data. Read Skill, Role, and Qualification lines. Personal-attribute lines and references are ignored and are not stored. Docs: https://www.brainiac.software/api/recruitment-operations/resume-data-extract",
      "parameters": {
        "type": "object",
        "properties": {
          "id": {
            "type": "string",
            "minLength": 1,
            "maxLength": 80
          },
          "name": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200
          },
          "text": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
          },
          "skills": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "years": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 80
                }
              },
              "required": [
                "name"
              ],
              "additionalProperties": false
            }
          },
          "roles": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "title": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "employer": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "start": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "end": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20
                },
                "text": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 2000
                }
              },
              "required": [
                "title",
                "employer"
              ],
              "additionalProperties": false
            }
          },
          "qualifications": {
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "year": {
                  "type": "integer",
                  "minimum": 1900,
                  "maximum": 2100
                }
              },
              "required": [
                "name"
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
      "name": "recruitment-operations__resume-job-match",
      "description": "Match a resume to a job. Compare supplied skills, qualifications, and role dates with explicit required items. A caller alias is marked inferred. A responsibility is not marked met. Docs: https://www.brainiac.software/api/recruitment-operations/resume-job-match",
      "parameters": {
        "type": "object",
        "properties": {
          "title": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200
          },
          "jobText": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
          },
          "requirements": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "enum": [
                    "skill",
                    "qualification",
                    "experience",
                    "responsibility"
                  ]
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "minimumYears": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 80
                },
                "strength": {
                  "type": "string",
                  "enum": [
                    "required",
                    "preferred"
                  ]
                }
              },
              "required": [
                "kind",
                "name"
              ],
              "additionalProperties": false
            }
          },
          "candidate": {
            "type": "object",
            "properties": {
              "id": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "name": {
                "type": "string",
                "minLength": 1,
                "maxLength": 200
              },
              "text": {
                "type": "string",
                "minLength": 1,
                "maxLength": 20000
              },
              "skills": {
                "maxItems": 40,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "name": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "years": {
                      "type": "number",
                      "minimum": 0,
                      "maximum": 80
                    }
                  },
                  "required": [
                    "name"
                  ],
                  "additionalProperties": false
                }
              },
              "roles": {
                "maxItems": 20,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "title": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "employer": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "start": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 20
                    },
                    "end": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 20
                    },
                    "text": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 2000
                    }
                  },
                  "required": [
                    "title",
                    "employer"
                  ],
                  "additionalProperties": false
                }
              },
              "qualifications": {
                "maxItems": 20,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "name": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "year": {
                      "type": "integer",
                      "minimum": 1900,
                      "maximum": 2100
                    }
                  },
                  "required": [
                    "name"
                  ],
                  "additionalProperties": false
                }
              }
            },
            "additionalProperties": false
          },
          "aliases": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "requirement": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "candidate": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                }
              },
              "required": [
                "requirement",
                "candidate"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "candidate"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "recruitment-operations__candidate-skill-compare",
      "description": "Compare candidate skills. Compare supplied skill names across candidates and against an explicit skill list. Missing skills are not invented. Docs: https://www.brainiac.software/api/recruitment-operations/candidate-skill-compare",
      "parameters": {
        "type": "object",
        "properties": {
          "skillNames": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 1,
              "maxLength": 200
            }
          },
          "candidates": {
            "minItems": 1,
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "text": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20000
                },
                "skills": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 200
                      },
                      "years": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 80
                      }
                    },
                    "required": [
                      "name"
                    ],
                    "additionalProperties": false
                  }
                },
                "roles": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "title": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 200
                      },
                      "employer": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 200
                      },
                      "start": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 20
                      },
                      "end": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 20
                      },
                      "text": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 2000
                      }
                    },
                    "required": [
                      "title",
                      "employer"
                    ],
                    "additionalProperties": false
                  }
                },
                "qualifications": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 200
                      },
                      "year": {
                        "type": "integer",
                        "minimum": 1900,
                        "maximum": 2100
                      }
                    },
                    "required": [
                      "name"
                    ],
                    "additionalProperties": false
                  }
                }
              },
              "additionalProperties": false
            }
          }
        },
        "required": [
          "candidates"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "recruitment-operations__candidate-experience-validate",
      "description": "Validate candidate experience. Check supplied employment dates for invalid dates, overlaps, and gaps. Dates are not rewritten, and a gap is not a ranking penalty. Docs: https://www.brainiac.software/api/recruitment-operations/candidate-experience-validate",
      "parameters": {
        "type": "object",
        "properties": {
          "candidates": {
            "minItems": 1,
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "text": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20000
                },
                "skills": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 200
                      },
                      "years": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 80
                      }
                    },
                    "required": [
                      "name"
                    ],
                    "additionalProperties": false
                  }
                },
                "roles": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "title": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 200
                      },
                      "employer": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 200
                      },
                      "start": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 20
                      },
                      "end": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 20
                      },
                      "text": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 2000
                      }
                    },
                    "required": [
                      "title",
                      "employer"
                    ],
                    "additionalProperties": false
                  }
                },
                "qualifications": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 200
                      },
                      "year": {
                        "type": "integer",
                        "minimum": 1900,
                        "maximum": 2100
                      }
                    },
                    "required": [
                      "name"
                    ],
                    "additionalProperties": false
                  }
                }
              },
              "additionalProperties": false
            }
          }
        },
        "required": [
          "candidates"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "recruitment-operations__interview-question-generate",
      "description": "Draft interview questions. Draft questions from missing required items, inferred alias matches, and job responsibilities. The questions do not score the candidate. Docs: https://www.brainiac.software/api/recruitment-operations/interview-question-generate",
      "parameters": {
        "type": "object",
        "properties": {
          "title": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200
          },
          "jobText": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
          },
          "requirements": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "enum": [
                    "skill",
                    "qualification",
                    "experience",
                    "responsibility"
                  ]
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "minimumYears": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 80
                },
                "strength": {
                  "type": "string",
                  "enum": [
                    "required",
                    "preferred"
                  ]
                }
              },
              "required": [
                "kind",
                "name"
              ],
              "additionalProperties": false
            }
          },
          "candidate": {
            "type": "object",
            "properties": {
              "id": {
                "type": "string",
                "minLength": 1,
                "maxLength": 80
              },
              "name": {
                "type": "string",
                "minLength": 1,
                "maxLength": 200
              },
              "text": {
                "type": "string",
                "minLength": 1,
                "maxLength": 20000
              },
              "skills": {
                "maxItems": 40,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "name": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "years": {
                      "type": "number",
                      "minimum": 0,
                      "maximum": 80
                    }
                  },
                  "required": [
                    "name"
                  ],
                  "additionalProperties": false
                }
              },
              "roles": {
                "maxItems": 20,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "title": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "employer": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "start": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 20
                    },
                    "end": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 20
                    },
                    "text": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 2000
                    }
                  },
                  "required": [
                    "title",
                    "employer"
                  ],
                  "additionalProperties": false
                }
              },
              "qualifications": {
                "maxItems": 20,
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "name": {
                      "type": "string",
                      "minLength": 1,
                      "maxLength": 200
                    },
                    "year": {
                      "type": "integer",
                      "minimum": 1900,
                      "maximum": 2100
                    }
                  },
                  "required": [
                    "name"
                  ],
                  "additionalProperties": false
                }
              }
            },
            "additionalProperties": false
          },
          "aliases": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "requirement": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "candidate": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                }
              },
              "required": [
                "requirement",
                "candidate"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "candidate"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "recruitment-operations__candidate-shortlist-rank",
      "description": "Rank a candidate shortlist. Score candidates only from explicit required matches. An exact match is worth 2 and a caller alias is worth 1. Ties keep the caller's order. Docs: https://www.brainiac.software/api/recruitment-operations/candidate-shortlist-rank",
      "parameters": {
        "type": "object",
        "properties": {
          "title": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200
          },
          "jobText": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
          },
          "requirements": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "enum": [
                    "skill",
                    "qualification",
                    "experience",
                    "responsibility"
                  ]
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "minimumYears": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 80
                },
                "strength": {
                  "type": "string",
                  "enum": [
                    "required",
                    "preferred"
                  ]
                }
              },
              "required": [
                "kind",
                "name"
              ],
              "additionalProperties": false
            }
          },
          "candidates": {
            "minItems": 1,
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "text": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20000
                },
                "skills": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 200
                      },
                      "years": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 80
                      }
                    },
                    "required": [
                      "name"
                    ],
                    "additionalProperties": false
                  }
                },
                "roles": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "title": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 200
                      },
                      "employer": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 200
                      },
                      "start": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 20
                      },
                      "end": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 20
                      },
                      "text": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 2000
                      }
                    },
                    "required": [
                      "title",
                      "employer"
                    ],
                    "additionalProperties": false
                  }
                },
                "qualifications": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 200
                      },
                      "year": {
                        "type": "integer",
                        "minimum": 1900,
                        "maximum": 2100
                      }
                    },
                    "required": [
                      "name"
                    ],
                    "additionalProperties": false
                  }
                }
              },
              "additionalProperties": false
            }
          },
          "aliases": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "requirement": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "candidate": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                }
              },
              "required": [
                "requirement",
                "candidate"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "candidates"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "recruitment-operations__pipeline-report",
      "description": "Report a recruitment pipeline. Combine the job requirements, resume facts, match explanations, experience checks, interview prompts, and shortlist scores. The report is not a hiring decision. Docs: https://www.brainiac.software/api/recruitment-operations/pipeline-report",
      "parameters": {
        "type": "object",
        "properties": {
          "title": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200
          },
          "jobText": {
            "type": "string",
            "minLength": 1,
            "maxLength": 20000
          },
          "requirements": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "kind": {
                  "type": "string",
                  "enum": [
                    "skill",
                    "qualification",
                    "experience",
                    "responsibility"
                  ]
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "minimumYears": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 80
                },
                "strength": {
                  "type": "string",
                  "enum": [
                    "required",
                    "preferred"
                  ]
                }
              },
              "required": [
                "kind",
                "name"
              ],
              "additionalProperties": false
            }
          },
          "candidates": {
            "minItems": 1,
            "maxItems": 20,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 80
                },
                "name": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "text": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 20000
                },
                "skills": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 200
                      },
                      "years": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 80
                      }
                    },
                    "required": [
                      "name"
                    ],
                    "additionalProperties": false
                  }
                },
                "roles": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "title": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 200
                      },
                      "employer": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 200
                      },
                      "start": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 20
                      },
                      "end": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 20
                      },
                      "text": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 2000
                      }
                    },
                    "required": [
                      "title",
                      "employer"
                    ],
                    "additionalProperties": false
                  }
                },
                "qualifications": {
                  "maxItems": 20,
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "name": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 200
                      },
                      "year": {
                        "type": "integer",
                        "minimum": 1900,
                        "maximum": 2100
                      }
                    },
                    "required": [
                      "name"
                    ],
                    "additionalProperties": false
                  }
                }
              },
              "additionalProperties": false
            }
          },
          "aliases": {
            "maxItems": 40,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "requirement": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                },
                "candidate": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 200
                }
              },
              "required": [
                "requirement",
                "candidate"
              ],
              "additionalProperties": false
            }
          }
        },
        "required": [
          "candidates"
        ]
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "recruitment-operations__job-description-structure": "0.03",
  "recruitment-operations__resume-data-extract": "0.04",
  "recruitment-operations__resume-job-match": "0.05",
  "recruitment-operations__candidate-skill-compare": "0.04",
  "recruitment-operations__candidate-experience-validate": "0.03",
  "recruitment-operations__interview-question-generate": "0.04",
  "recruitment-operations__candidate-shortlist-rank": "0.05",
  "recruitment-operations__pipeline-report": "0.12"
}
TOOL_ROUTES: Dict[str, str] = {
  "recruitment-operations__job-description-structure": "recruitment-operations/job-description-structure",
  "recruitment-operations__resume-data-extract": "recruitment-operations/resume-data-extract",
  "recruitment-operations__resume-job-match": "recruitment-operations/resume-job-match",
  "recruitment-operations__candidate-skill-compare": "recruitment-operations/candidate-skill-compare",
  "recruitment-operations__candidate-experience-validate": "recruitment-operations/candidate-experience-validate",
  "recruitment-operations__interview-question-generate": "recruitment-operations/interview-question-generate",
  "recruitment-operations__candidate-shortlist-rank": "recruitment-operations/candidate-shortlist-rank",
  "recruitment-operations__pipeline-report": "recruitment-operations/pipeline-report"
}


class BrainiacRecruitmentOperationsAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — recruitment-operations",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the recruitment-operations catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "recruitment-operations", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Structure a job description"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.03",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the recruitment-operations group. "
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
