"""Auto-generated BRAINIAC Heurist Mesh agent for group `fraud-signals` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "fraud-signals__payment-fraud-pattern-detect",
      "description": "Detect payment fraud patterns. Detect suspicious combinations of caller-supplied payment events (declines-then-success, instrument churn, billing/shipping mismatch). Anomalies are not confirmed fraud. Docs: https://www.brainiac.software/api/fraud-signals/payment-fraud-pattern-detect",
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
                  "application/json",
                  "application/octet-stream"
                ]
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              },
              "role": {
                "type": "string",
                "maxLength": 80
              }
            },
            "required": [
              "fileBase64"
            ],
            "additionalProperties": false
          },
          "files": {
            "maxItems": 20,
            "type": "array",
            "items": {
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
                    "application/json",
                    "application/octet-stream"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "payments": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "accountId": {
                  "type": "string",
                  "maxLength": 120
                },
                "customerId": {
                  "type": "string",
                  "maxLength": 120
                },
                "merchantId": {
                  "type": "string",
                  "maxLength": 120
                },
                "eventType": {
                  "type": "string",
                  "maxLength": 80
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "paymentMethod": {
                  "type": "string",
                  "maxLength": 80
                },
                "cardLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "cardBin": {
                  "type": "string",
                  "maxLength": 8
                },
                "panToken": {
                  "type": "string",
                  "maxLength": 80
                },
                "bankAccountLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "bankRoutingLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "ibanLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "email": {
                  "type": "string",
                  "maxLength": 254
                },
                "phone": {
                  "type": "string",
                  "maxLength": 40
                },
                "billingCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "shippingCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "invoiceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 120
                },
                "reason": {
                  "type": "string",
                  "maxLength": 300
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "transactions": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "accountId": {
                  "type": "string",
                  "maxLength": 120
                },
                "customerId": {
                  "type": "string",
                  "maxLength": 120
                },
                "merchantId": {
                  "type": "string",
                  "maxLength": 120
                },
                "eventType": {
                  "type": "string",
                  "maxLength": 80
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "paymentMethod": {
                  "type": "string",
                  "maxLength": 80
                },
                "cardLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "cardBin": {
                  "type": "string",
                  "maxLength": 8
                },
                "panToken": {
                  "type": "string",
                  "maxLength": 80
                },
                "bankAccountLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "bankRoutingLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "ibanLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "email": {
                  "type": "string",
                  "maxLength": 254
                },
                "phone": {
                  "type": "string",
                  "maxLength": 40
                },
                "billingCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "shippingCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "invoiceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 120
                },
                "reason": {
                  "type": "string",
                  "maxLength": 300
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "identities": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "accountId": {
                  "type": "string",
                  "maxLength": 120
                },
                "fullName": {
                  "type": "string",
                  "maxLength": 200
                },
                "email": {
                  "type": "string",
                  "maxLength": 254
                },
                "phone": {
                  "type": "string",
                  "maxLength": 40
                },
                "dateOfBirth": {
                  "type": "string",
                  "maxLength": 40
                },
                "addressLine": {
                  "type": "string",
                  "maxLength": 300
                },
                "city": {
                  "type": "string",
                  "maxLength": 120
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "postalCode": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "nationalIdLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "createdAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "invoices": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 120
                },
                "supplierName": {
                  "type": "string",
                  "maxLength": 200
                },
                "customerId": {
                  "type": "string",
                  "maxLength": 120
                },
                "invoiceNumber": {
                  "type": "string",
                  "maxLength": 120
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "taxAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "lineCount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "bankAccountLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "bankRoutingLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "ibanLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "previousBankAccountLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "previousBankRoutingLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "previousIbanLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "bankChangedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "poNumber": {
                  "type": "string",
                  "maxLength": 120
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "duplicateOf": {
                  "type": "string",
                  "maxLength": 80
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "velocityWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "velocityCountThreshold": {
            "type": "number",
            "minimum": 2,
            "maximum": 10000
          },
          "velocityAmountThreshold": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000
          },
          "refundWindowDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 365
          },
          "chargebackWindowDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 730
          },
          "bankChangeRiskHours": {
            "type": "number",
            "minimum": 1,
            "maximum": 2160
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "fraud-signals__transaction-velocity-analyze",
      "description": "Analyze transaction velocity. Identify abnormal transaction frequency and amount velocity from caller-supplied histories. Velocity spikes alone are never labeled confirmed fraud. Docs: https://www.brainiac.software/api/fraud-signals/transaction-velocity-analyze",
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
                  "application/json",
                  "application/octet-stream"
                ]
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              },
              "role": {
                "type": "string",
                "maxLength": 80
              }
            },
            "required": [
              "fileBase64"
            ],
            "additionalProperties": false
          },
          "files": {
            "maxItems": 20,
            "type": "array",
            "items": {
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
                    "application/json",
                    "application/octet-stream"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "payments": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "accountId": {
                  "type": "string",
                  "maxLength": 120
                },
                "customerId": {
                  "type": "string",
                  "maxLength": 120
                },
                "merchantId": {
                  "type": "string",
                  "maxLength": 120
                },
                "eventType": {
                  "type": "string",
                  "maxLength": 80
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "paymentMethod": {
                  "type": "string",
                  "maxLength": 80
                },
                "cardLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "cardBin": {
                  "type": "string",
                  "maxLength": 8
                },
                "panToken": {
                  "type": "string",
                  "maxLength": 80
                },
                "bankAccountLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "bankRoutingLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "ibanLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "email": {
                  "type": "string",
                  "maxLength": 254
                },
                "phone": {
                  "type": "string",
                  "maxLength": 40
                },
                "billingCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "shippingCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "invoiceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 120
                },
                "reason": {
                  "type": "string",
                  "maxLength": 300
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "transactions": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "accountId": {
                  "type": "string",
                  "maxLength": 120
                },
                "customerId": {
                  "type": "string",
                  "maxLength": 120
                },
                "merchantId": {
                  "type": "string",
                  "maxLength": 120
                },
                "eventType": {
                  "type": "string",
                  "maxLength": 80
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "paymentMethod": {
                  "type": "string",
                  "maxLength": 80
                },
                "cardLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "cardBin": {
                  "type": "string",
                  "maxLength": 8
                },
                "panToken": {
                  "type": "string",
                  "maxLength": 80
                },
                "bankAccountLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "bankRoutingLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "ibanLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "email": {
                  "type": "string",
                  "maxLength": 254
                },
                "phone": {
                  "type": "string",
                  "maxLength": 40
                },
                "billingCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "shippingCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "invoiceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 120
                },
                "reason": {
                  "type": "string",
                  "maxLength": 300
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "identities": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "accountId": {
                  "type": "string",
                  "maxLength": 120
                },
                "fullName": {
                  "type": "string",
                  "maxLength": 200
                },
                "email": {
                  "type": "string",
                  "maxLength": 254
                },
                "phone": {
                  "type": "string",
                  "maxLength": 40
                },
                "dateOfBirth": {
                  "type": "string",
                  "maxLength": 40
                },
                "addressLine": {
                  "type": "string",
                  "maxLength": 300
                },
                "city": {
                  "type": "string",
                  "maxLength": 120
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "postalCode": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "nationalIdLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "createdAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "invoices": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 120
                },
                "supplierName": {
                  "type": "string",
                  "maxLength": 200
                },
                "customerId": {
                  "type": "string",
                  "maxLength": 120
                },
                "invoiceNumber": {
                  "type": "string",
                  "maxLength": 120
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "taxAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "lineCount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "bankAccountLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "bankRoutingLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "ibanLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "previousBankAccountLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "previousBankRoutingLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "previousIbanLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "bankChangedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "poNumber": {
                  "type": "string",
                  "maxLength": 120
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "duplicateOf": {
                  "type": "string",
                  "maxLength": 80
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "velocityWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "velocityCountThreshold": {
            "type": "number",
            "minimum": 2,
            "maximum": 10000
          },
          "velocityAmountThreshold": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000
          },
          "refundWindowDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 365
          },
          "chargebackWindowDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 730
          },
          "bankChangeRiskHours": {
            "type": "number",
            "minimum": 1,
            "maximum": 2160
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "fraud-signals__synthetic-identity-signal-detect",
      "description": "Detect synthetic-identity signals. Identify inconsistencies in caller-supplied identity records (sparse profiles, age/postal mismatches, shared contacts). Personal data is masked in responses. Docs: https://www.brainiac.software/api/fraud-signals/synthetic-identity-signal-detect",
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
                  "application/json",
                  "application/octet-stream"
                ]
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              },
              "role": {
                "type": "string",
                "maxLength": 80
              }
            },
            "required": [
              "fileBase64"
            ],
            "additionalProperties": false
          },
          "files": {
            "maxItems": 20,
            "type": "array",
            "items": {
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
                    "application/json",
                    "application/octet-stream"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "payments": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "accountId": {
                  "type": "string",
                  "maxLength": 120
                },
                "customerId": {
                  "type": "string",
                  "maxLength": 120
                },
                "merchantId": {
                  "type": "string",
                  "maxLength": 120
                },
                "eventType": {
                  "type": "string",
                  "maxLength": 80
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "paymentMethod": {
                  "type": "string",
                  "maxLength": 80
                },
                "cardLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "cardBin": {
                  "type": "string",
                  "maxLength": 8
                },
                "panToken": {
                  "type": "string",
                  "maxLength": 80
                },
                "bankAccountLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "bankRoutingLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "ibanLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "email": {
                  "type": "string",
                  "maxLength": 254
                },
                "phone": {
                  "type": "string",
                  "maxLength": 40
                },
                "billingCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "shippingCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "invoiceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 120
                },
                "reason": {
                  "type": "string",
                  "maxLength": 300
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "transactions": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "accountId": {
                  "type": "string",
                  "maxLength": 120
                },
                "customerId": {
                  "type": "string",
                  "maxLength": 120
                },
                "merchantId": {
                  "type": "string",
                  "maxLength": 120
                },
                "eventType": {
                  "type": "string",
                  "maxLength": 80
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "paymentMethod": {
                  "type": "string",
                  "maxLength": 80
                },
                "cardLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "cardBin": {
                  "type": "string",
                  "maxLength": 8
                },
                "panToken": {
                  "type": "string",
                  "maxLength": 80
                },
                "bankAccountLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "bankRoutingLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "ibanLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "email": {
                  "type": "string",
                  "maxLength": 254
                },
                "phone": {
                  "type": "string",
                  "maxLength": 40
                },
                "billingCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "shippingCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "invoiceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 120
                },
                "reason": {
                  "type": "string",
                  "maxLength": 300
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "identities": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "accountId": {
                  "type": "string",
                  "maxLength": 120
                },
                "fullName": {
                  "type": "string",
                  "maxLength": 200
                },
                "email": {
                  "type": "string",
                  "maxLength": 254
                },
                "phone": {
                  "type": "string",
                  "maxLength": 40
                },
                "dateOfBirth": {
                  "type": "string",
                  "maxLength": 40
                },
                "addressLine": {
                  "type": "string",
                  "maxLength": 300
                },
                "city": {
                  "type": "string",
                  "maxLength": 120
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "postalCode": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "nationalIdLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "createdAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "invoices": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 120
                },
                "supplierName": {
                  "type": "string",
                  "maxLength": 200
                },
                "customerId": {
                  "type": "string",
                  "maxLength": 120
                },
                "invoiceNumber": {
                  "type": "string",
                  "maxLength": 120
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "taxAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "lineCount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "bankAccountLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "bankRoutingLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "ibanLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "previousBankAccountLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "previousBankRoutingLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "previousIbanLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "bankChangedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "poNumber": {
                  "type": "string",
                  "maxLength": 120
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "duplicateOf": {
                  "type": "string",
                  "maxLength": 80
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "velocityWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "velocityCountThreshold": {
            "type": "number",
            "minimum": 2,
            "maximum": 10000
          },
          "velocityAmountThreshold": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000
          },
          "refundWindowDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 365
          },
          "chargebackWindowDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 730
          },
          "bankChangeRiskHours": {
            "type": "number",
            "minimum": 1,
            "maximum": 2160
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "fraud-signals__invoice-fraud-signal-detect",
      "description": "Detect invoice fraud signals. Detect potentially manipulated invoices from caller-supplied invoice exports (duplicate numbers, tax anomalies, missing PO). Not confirmed fraud. Docs: https://www.brainiac.software/api/fraud-signals/invoice-fraud-signal-detect",
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
                  "application/json",
                  "application/octet-stream"
                ]
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              },
              "role": {
                "type": "string",
                "maxLength": 80
              }
            },
            "required": [
              "fileBase64"
            ],
            "additionalProperties": false
          },
          "files": {
            "maxItems": 20,
            "type": "array",
            "items": {
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
                    "application/json",
                    "application/octet-stream"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "payments": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "accountId": {
                  "type": "string",
                  "maxLength": 120
                },
                "customerId": {
                  "type": "string",
                  "maxLength": 120
                },
                "merchantId": {
                  "type": "string",
                  "maxLength": 120
                },
                "eventType": {
                  "type": "string",
                  "maxLength": 80
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "paymentMethod": {
                  "type": "string",
                  "maxLength": 80
                },
                "cardLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "cardBin": {
                  "type": "string",
                  "maxLength": 8
                },
                "panToken": {
                  "type": "string",
                  "maxLength": 80
                },
                "bankAccountLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "bankRoutingLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "ibanLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "email": {
                  "type": "string",
                  "maxLength": 254
                },
                "phone": {
                  "type": "string",
                  "maxLength": 40
                },
                "billingCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "shippingCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "invoiceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 120
                },
                "reason": {
                  "type": "string",
                  "maxLength": 300
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "transactions": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "accountId": {
                  "type": "string",
                  "maxLength": 120
                },
                "customerId": {
                  "type": "string",
                  "maxLength": 120
                },
                "merchantId": {
                  "type": "string",
                  "maxLength": 120
                },
                "eventType": {
                  "type": "string",
                  "maxLength": 80
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "paymentMethod": {
                  "type": "string",
                  "maxLength": 80
                },
                "cardLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "cardBin": {
                  "type": "string",
                  "maxLength": 8
                },
                "panToken": {
                  "type": "string",
                  "maxLength": 80
                },
                "bankAccountLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "bankRoutingLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "ibanLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "email": {
                  "type": "string",
                  "maxLength": 254
                },
                "phone": {
                  "type": "string",
                  "maxLength": 40
                },
                "billingCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "shippingCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "invoiceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 120
                },
                "reason": {
                  "type": "string",
                  "maxLength": 300
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "identities": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "accountId": {
                  "type": "string",
                  "maxLength": 120
                },
                "fullName": {
                  "type": "string",
                  "maxLength": 200
                },
                "email": {
                  "type": "string",
                  "maxLength": 254
                },
                "phone": {
                  "type": "string",
                  "maxLength": 40
                },
                "dateOfBirth": {
                  "type": "string",
                  "maxLength": 40
                },
                "addressLine": {
                  "type": "string",
                  "maxLength": 300
                },
                "city": {
                  "type": "string",
                  "maxLength": 120
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "postalCode": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "nationalIdLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "createdAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "invoices": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 120
                },
                "supplierName": {
                  "type": "string",
                  "maxLength": 200
                },
                "customerId": {
                  "type": "string",
                  "maxLength": 120
                },
                "invoiceNumber": {
                  "type": "string",
                  "maxLength": 120
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "taxAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "lineCount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "bankAccountLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "bankRoutingLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "ibanLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "previousBankAccountLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "previousBankRoutingLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "previousIbanLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "bankChangedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "poNumber": {
                  "type": "string",
                  "maxLength": 120
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "duplicateOf": {
                  "type": "string",
                  "maxLength": 80
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "velocityWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "velocityCountThreshold": {
            "type": "number",
            "minimum": 2,
            "maximum": 10000
          },
          "velocityAmountThreshold": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000
          },
          "refundWindowDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 365
          },
          "chargebackWindowDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 730
          },
          "bankChangeRiskHours": {
            "type": "number",
            "minimum": 1,
            "maximum": 2160
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "fraud-signals__supplier-bank-change-risk",
      "description": "Assess supplier bank-change risk. Identify suspicious supplier bank-detail changes near invoice timing from caller-supplied records. Bank values are last4-masked. Docs: https://www.brainiac.software/api/fraud-signals/supplier-bank-change-risk",
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
                  "application/json",
                  "application/octet-stream"
                ]
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              },
              "role": {
                "type": "string",
                "maxLength": 80
              }
            },
            "required": [
              "fileBase64"
            ],
            "additionalProperties": false
          },
          "files": {
            "maxItems": 20,
            "type": "array",
            "items": {
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
                    "application/json",
                    "application/octet-stream"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "payments": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "accountId": {
                  "type": "string",
                  "maxLength": 120
                },
                "customerId": {
                  "type": "string",
                  "maxLength": 120
                },
                "merchantId": {
                  "type": "string",
                  "maxLength": 120
                },
                "eventType": {
                  "type": "string",
                  "maxLength": 80
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "paymentMethod": {
                  "type": "string",
                  "maxLength": 80
                },
                "cardLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "cardBin": {
                  "type": "string",
                  "maxLength": 8
                },
                "panToken": {
                  "type": "string",
                  "maxLength": 80
                },
                "bankAccountLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "bankRoutingLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "ibanLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "email": {
                  "type": "string",
                  "maxLength": 254
                },
                "phone": {
                  "type": "string",
                  "maxLength": 40
                },
                "billingCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "shippingCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "invoiceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 120
                },
                "reason": {
                  "type": "string",
                  "maxLength": 300
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "transactions": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "accountId": {
                  "type": "string",
                  "maxLength": 120
                },
                "customerId": {
                  "type": "string",
                  "maxLength": 120
                },
                "merchantId": {
                  "type": "string",
                  "maxLength": 120
                },
                "eventType": {
                  "type": "string",
                  "maxLength": 80
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "paymentMethod": {
                  "type": "string",
                  "maxLength": 80
                },
                "cardLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "cardBin": {
                  "type": "string",
                  "maxLength": 8
                },
                "panToken": {
                  "type": "string",
                  "maxLength": 80
                },
                "bankAccountLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "bankRoutingLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "ibanLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "email": {
                  "type": "string",
                  "maxLength": 254
                },
                "phone": {
                  "type": "string",
                  "maxLength": 40
                },
                "billingCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "shippingCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "invoiceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 120
                },
                "reason": {
                  "type": "string",
                  "maxLength": 300
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "identities": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "accountId": {
                  "type": "string",
                  "maxLength": 120
                },
                "fullName": {
                  "type": "string",
                  "maxLength": 200
                },
                "email": {
                  "type": "string",
                  "maxLength": 254
                },
                "phone": {
                  "type": "string",
                  "maxLength": 40
                },
                "dateOfBirth": {
                  "type": "string",
                  "maxLength": 40
                },
                "addressLine": {
                  "type": "string",
                  "maxLength": 300
                },
                "city": {
                  "type": "string",
                  "maxLength": 120
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "postalCode": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "nationalIdLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "createdAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "invoices": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 120
                },
                "supplierName": {
                  "type": "string",
                  "maxLength": 200
                },
                "customerId": {
                  "type": "string",
                  "maxLength": 120
                },
                "invoiceNumber": {
                  "type": "string",
                  "maxLength": 120
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "taxAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "lineCount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "bankAccountLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "bankRoutingLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "ibanLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "previousBankAccountLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "previousBankRoutingLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "previousIbanLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "bankChangedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "poNumber": {
                  "type": "string",
                  "maxLength": 120
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "duplicateOf": {
                  "type": "string",
                  "maxLength": 80
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "velocityWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "velocityCountThreshold": {
            "type": "number",
            "minimum": 2,
            "maximum": 10000
          },
          "velocityAmountThreshold": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000
          },
          "refundWindowDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 365
          },
          "chargebackWindowDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 730
          },
          "bankChangeRiskHours": {
            "type": "number",
            "minimum": 1,
            "maximum": 2160
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "fraud-signals__refund-abuse-pattern-detect",
      "description": "Detect refund-abuse patterns. Detect abnormal refund frequency and amount ratios from caller-supplied payment histories. Refund rate alone is not confirmed fraud. Docs: https://www.brainiac.software/api/fraud-signals/refund-abuse-pattern-detect",
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
                  "application/json",
                  "application/octet-stream"
                ]
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              },
              "role": {
                "type": "string",
                "maxLength": 80
              }
            },
            "required": [
              "fileBase64"
            ],
            "additionalProperties": false
          },
          "files": {
            "maxItems": 20,
            "type": "array",
            "items": {
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
                    "application/json",
                    "application/octet-stream"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "payments": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "accountId": {
                  "type": "string",
                  "maxLength": 120
                },
                "customerId": {
                  "type": "string",
                  "maxLength": 120
                },
                "merchantId": {
                  "type": "string",
                  "maxLength": 120
                },
                "eventType": {
                  "type": "string",
                  "maxLength": 80
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "paymentMethod": {
                  "type": "string",
                  "maxLength": 80
                },
                "cardLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "cardBin": {
                  "type": "string",
                  "maxLength": 8
                },
                "panToken": {
                  "type": "string",
                  "maxLength": 80
                },
                "bankAccountLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "bankRoutingLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "ibanLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "email": {
                  "type": "string",
                  "maxLength": 254
                },
                "phone": {
                  "type": "string",
                  "maxLength": 40
                },
                "billingCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "shippingCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "invoiceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 120
                },
                "reason": {
                  "type": "string",
                  "maxLength": 300
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "transactions": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "accountId": {
                  "type": "string",
                  "maxLength": 120
                },
                "customerId": {
                  "type": "string",
                  "maxLength": 120
                },
                "merchantId": {
                  "type": "string",
                  "maxLength": 120
                },
                "eventType": {
                  "type": "string",
                  "maxLength": 80
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "paymentMethod": {
                  "type": "string",
                  "maxLength": 80
                },
                "cardLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "cardBin": {
                  "type": "string",
                  "maxLength": 8
                },
                "panToken": {
                  "type": "string",
                  "maxLength": 80
                },
                "bankAccountLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "bankRoutingLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "ibanLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "email": {
                  "type": "string",
                  "maxLength": 254
                },
                "phone": {
                  "type": "string",
                  "maxLength": 40
                },
                "billingCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "shippingCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "invoiceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 120
                },
                "reason": {
                  "type": "string",
                  "maxLength": 300
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "identities": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "accountId": {
                  "type": "string",
                  "maxLength": 120
                },
                "fullName": {
                  "type": "string",
                  "maxLength": 200
                },
                "email": {
                  "type": "string",
                  "maxLength": 254
                },
                "phone": {
                  "type": "string",
                  "maxLength": 40
                },
                "dateOfBirth": {
                  "type": "string",
                  "maxLength": 40
                },
                "addressLine": {
                  "type": "string",
                  "maxLength": 300
                },
                "city": {
                  "type": "string",
                  "maxLength": 120
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "postalCode": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "nationalIdLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "createdAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "invoices": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 120
                },
                "supplierName": {
                  "type": "string",
                  "maxLength": 200
                },
                "customerId": {
                  "type": "string",
                  "maxLength": 120
                },
                "invoiceNumber": {
                  "type": "string",
                  "maxLength": 120
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "taxAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "lineCount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "bankAccountLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "bankRoutingLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "ibanLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "previousBankAccountLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "previousBankRoutingLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "previousIbanLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "bankChangedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "poNumber": {
                  "type": "string",
                  "maxLength": 120
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "duplicateOf": {
                  "type": "string",
                  "maxLength": 80
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "velocityWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "velocityCountThreshold": {
            "type": "number",
            "minimum": 2,
            "maximum": 10000
          },
          "velocityAmountThreshold": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000
          },
          "refundWindowDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 365
          },
          "chargebackWindowDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 730
          },
          "bankChangeRiskHours": {
            "type": "number",
            "minimum": 1,
            "maximum": 2160
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "fraud-signals__chargeback-pattern-analyze",
      "description": "Analyze chargeback patterns. Analyze recurring chargeback/dispute patterns from caller-supplied payment records. Elevated rates are indicators, not confirmed fraud. Docs: https://www.brainiac.software/api/fraud-signals/chargeback-pattern-analyze",
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
                  "application/json",
                  "application/octet-stream"
                ]
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              },
              "role": {
                "type": "string",
                "maxLength": 80
              }
            },
            "required": [
              "fileBase64"
            ],
            "additionalProperties": false
          },
          "files": {
            "maxItems": 20,
            "type": "array",
            "items": {
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
                    "application/json",
                    "application/octet-stream"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "payments": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "accountId": {
                  "type": "string",
                  "maxLength": 120
                },
                "customerId": {
                  "type": "string",
                  "maxLength": 120
                },
                "merchantId": {
                  "type": "string",
                  "maxLength": 120
                },
                "eventType": {
                  "type": "string",
                  "maxLength": 80
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "paymentMethod": {
                  "type": "string",
                  "maxLength": 80
                },
                "cardLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "cardBin": {
                  "type": "string",
                  "maxLength": 8
                },
                "panToken": {
                  "type": "string",
                  "maxLength": 80
                },
                "bankAccountLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "bankRoutingLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "ibanLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "email": {
                  "type": "string",
                  "maxLength": 254
                },
                "phone": {
                  "type": "string",
                  "maxLength": 40
                },
                "billingCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "shippingCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "invoiceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 120
                },
                "reason": {
                  "type": "string",
                  "maxLength": 300
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "transactions": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "accountId": {
                  "type": "string",
                  "maxLength": 120
                },
                "customerId": {
                  "type": "string",
                  "maxLength": 120
                },
                "merchantId": {
                  "type": "string",
                  "maxLength": 120
                },
                "eventType": {
                  "type": "string",
                  "maxLength": 80
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "paymentMethod": {
                  "type": "string",
                  "maxLength": 80
                },
                "cardLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "cardBin": {
                  "type": "string",
                  "maxLength": 8
                },
                "panToken": {
                  "type": "string",
                  "maxLength": 80
                },
                "bankAccountLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "bankRoutingLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "ibanLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "email": {
                  "type": "string",
                  "maxLength": 254
                },
                "phone": {
                  "type": "string",
                  "maxLength": 40
                },
                "billingCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "shippingCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "invoiceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 120
                },
                "reason": {
                  "type": "string",
                  "maxLength": 300
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "identities": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "accountId": {
                  "type": "string",
                  "maxLength": 120
                },
                "fullName": {
                  "type": "string",
                  "maxLength": 200
                },
                "email": {
                  "type": "string",
                  "maxLength": 254
                },
                "phone": {
                  "type": "string",
                  "maxLength": 40
                },
                "dateOfBirth": {
                  "type": "string",
                  "maxLength": 40
                },
                "addressLine": {
                  "type": "string",
                  "maxLength": 300
                },
                "city": {
                  "type": "string",
                  "maxLength": 120
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "postalCode": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "nationalIdLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "createdAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "invoices": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 120
                },
                "supplierName": {
                  "type": "string",
                  "maxLength": 200
                },
                "customerId": {
                  "type": "string",
                  "maxLength": 120
                },
                "invoiceNumber": {
                  "type": "string",
                  "maxLength": 120
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "taxAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "lineCount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "bankAccountLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "bankRoutingLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "ibanLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "previousBankAccountLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "previousBankRoutingLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "previousIbanLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "bankChangedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "poNumber": {
                  "type": "string",
                  "maxLength": 120
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "duplicateOf": {
                  "type": "string",
                  "maxLength": 80
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "velocityWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "velocityCountThreshold": {
            "type": "number",
            "minimum": 2,
            "maximum": 10000
          },
          "velocityAmountThreshold": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000
          },
          "refundWindowDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 365
          },
          "chargebackWindowDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 730
          },
          "bankChangeRiskHours": {
            "type": "number",
            "minimum": 1,
            "maximum": 2160
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "fraud-signals__multi-account-fraud-cluster",
      "description": "Cluster related fraud accounts. Group potentially related accounts using deterministic overlap of caller-supplied emails, phones, devices, IPs, and payment-instrument last4 values. Linkage is not confirmed fraud. Docs: https://www.brainiac.software/api/fraud-signals/multi-account-fraud-cluster",
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
                  "application/json",
                  "application/octet-stream"
                ]
              },
              "fileBase64": {
                "type": "string",
                "minLength": 1,
                "maxLength": 12000000
              },
              "role": {
                "type": "string",
                "maxLength": 80
              }
            },
            "required": [
              "fileBase64"
            ],
            "additionalProperties": false
          },
          "files": {
            "maxItems": 20,
            "type": "array",
            "items": {
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
                    "application/json",
                    "application/octet-stream"
                  ]
                },
                "fileBase64": {
                  "type": "string",
                  "minLength": 1,
                  "maxLength": 12000000
                },
                "role": {
                  "type": "string",
                  "maxLength": 80
                }
              },
              "required": [
                "fileBase64"
              ],
              "additionalProperties": false
            }
          },
          "payments": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "accountId": {
                  "type": "string",
                  "maxLength": 120
                },
                "customerId": {
                  "type": "string",
                  "maxLength": 120
                },
                "merchantId": {
                  "type": "string",
                  "maxLength": 120
                },
                "eventType": {
                  "type": "string",
                  "maxLength": 80
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "paymentMethod": {
                  "type": "string",
                  "maxLength": 80
                },
                "cardLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "cardBin": {
                  "type": "string",
                  "maxLength": 8
                },
                "panToken": {
                  "type": "string",
                  "maxLength": 80
                },
                "bankAccountLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "bankRoutingLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "ibanLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "email": {
                  "type": "string",
                  "maxLength": 254
                },
                "phone": {
                  "type": "string",
                  "maxLength": 40
                },
                "billingCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "shippingCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "invoiceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 120
                },
                "reason": {
                  "type": "string",
                  "maxLength": 300
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "transactions": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "accountId": {
                  "type": "string",
                  "maxLength": 120
                },
                "customerId": {
                  "type": "string",
                  "maxLength": 120
                },
                "merchantId": {
                  "type": "string",
                  "maxLength": 120
                },
                "eventType": {
                  "type": "string",
                  "maxLength": 80
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "paymentMethod": {
                  "type": "string",
                  "maxLength": 80
                },
                "cardLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "cardBin": {
                  "type": "string",
                  "maxLength": 8
                },
                "panToken": {
                  "type": "string",
                  "maxLength": 80
                },
                "bankAccountLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "bankRoutingLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "ibanLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "email": {
                  "type": "string",
                  "maxLength": 254
                },
                "phone": {
                  "type": "string",
                  "maxLength": 40
                },
                "billingCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "shippingCountry": {
                  "type": "string",
                  "maxLength": 80
                },
                "invoiceId": {
                  "type": "string",
                  "maxLength": 80
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 120
                },
                "reason": {
                  "type": "string",
                  "maxLength": 300
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "identities": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "accountId": {
                  "type": "string",
                  "maxLength": 120
                },
                "fullName": {
                  "type": "string",
                  "maxLength": 200
                },
                "email": {
                  "type": "string",
                  "maxLength": 254
                },
                "phone": {
                  "type": "string",
                  "maxLength": 40
                },
                "dateOfBirth": {
                  "type": "string",
                  "maxLength": 40
                },
                "addressLine": {
                  "type": "string",
                  "maxLength": 300
                },
                "city": {
                  "type": "string",
                  "maxLength": 120
                },
                "region": {
                  "type": "string",
                  "maxLength": 120
                },
                "postalCode": {
                  "type": "string",
                  "maxLength": 40
                },
                "country": {
                  "type": "string",
                  "maxLength": 80
                },
                "nationalIdLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "deviceId": {
                  "type": "string",
                  "maxLength": 120
                },
                "ip": {
                  "type": "string",
                  "maxLength": 80
                },
                "createdAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "invoices": {
            "maxItems": 20000,
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "id": {
                  "type": "string",
                  "maxLength": 80
                },
                "at": {
                  "type": "string",
                  "maxLength": 40
                },
                "supplierId": {
                  "type": "string",
                  "maxLength": 120
                },
                "supplierName": {
                  "type": "string",
                  "maxLength": 200
                },
                "customerId": {
                  "type": "string",
                  "maxLength": 120
                },
                "invoiceNumber": {
                  "type": "string",
                  "maxLength": 120
                },
                "amount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "currency": {
                  "type": "string",
                  "maxLength": 12
                },
                "taxAmount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 1000000000
                },
                "lineCount": {
                  "type": "number",
                  "minimum": 0,
                  "maximum": 100000
                },
                "bankAccountLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "bankRoutingLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "ibanLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "previousBankAccountLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "previousBankRoutingLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "previousIbanLast4": {
                  "type": "string",
                  "maxLength": 4
                },
                "bankChangedAt": {
                  "type": "string",
                  "maxLength": 40
                },
                "poNumber": {
                  "type": "string",
                  "maxLength": 120
                },
                "status": {
                  "type": "string",
                  "maxLength": 80
                },
                "duplicateOf": {
                  "type": "string",
                  "maxLength": 80
                },
                "labels": {
                  "maxItems": 40,
                  "type": "array",
                  "items": {
                    "type": "string",
                    "maxLength": 80
                  }
                },
                "source": {
                  "type": "string",
                  "maxLength": 200
                }
              },
              "additionalProperties": false
            }
          },
          "asOf": {
            "type": "string",
            "maxLength": 40
          },
          "velocityWindowMinutes": {
            "type": "number",
            "minimum": 1,
            "maximum": 10080
          },
          "velocityCountThreshold": {
            "type": "number",
            "minimum": 2,
            "maximum": 10000
          },
          "velocityAmountThreshold": {
            "type": "number",
            "minimum": 0,
            "maximum": 1000000000
          },
          "refundWindowDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 365
          },
          "chargebackWindowDays": {
            "type": "number",
            "minimum": 1,
            "maximum": 730
          },
          "bankChangeRiskHours": {
            "type": "number",
            "minimum": 1,
            "maximum": 2160
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "fraud-signals__payment-fraud-pattern-detect": "0.05",
  "fraud-signals__transaction-velocity-analyze": "0.04",
  "fraud-signals__synthetic-identity-signal-detect": "0.04",
  "fraud-signals__invoice-fraud-signal-detect": "0.04",
  "fraud-signals__supplier-bank-change-risk": "0.04",
  "fraud-signals__refund-abuse-pattern-detect": "0.04",
  "fraud-signals__chargeback-pattern-analyze": "0.04",
  "fraud-signals__multi-account-fraud-cluster": "0.05"
}
TOOL_ROUTES: Dict[str, str] = {
  "fraud-signals__payment-fraud-pattern-detect": "fraud-signals/payment-fraud-pattern-detect",
  "fraud-signals__transaction-velocity-analyze": "fraud-signals/transaction-velocity-analyze",
  "fraud-signals__synthetic-identity-signal-detect": "fraud-signals/synthetic-identity-signal-detect",
  "fraud-signals__invoice-fraud-signal-detect": "fraud-signals/invoice-fraud-signal-detect",
  "fraud-signals__supplier-bank-change-risk": "fraud-signals/supplier-bank-change-risk",
  "fraud-signals__refund-abuse-pattern-detect": "fraud-signals/refund-abuse-pattern-detect",
  "fraud-signals__chargeback-pattern-analyze": "fraud-signals/chargeback-pattern-analyze",
  "fraud-signals__multi-account-fraud-cluster": "fraud-signals/multi-account-fraud-cluster"
}


class BrainiacFraudSignalsAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — fraud-signals",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the fraud-signals catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "fraud-signals", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Detect payment fraud patterns"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.04",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the fraud-signals group. "
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
