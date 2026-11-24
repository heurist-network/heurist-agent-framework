"""Auto-generated BRAINIAC Heurist Mesh agent for group `chain-data` (#224). Do not edit by hand — regenerate via integrations/heurist-mesh/generate.ts."""
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
      "name": "chain-data__network-info",
      "description": "Get network information. Retrieve Base Mainnet chain ID and network information from the public JSON-RPC endpoint. Docs: https://www.brainiac.software/api/chain-data/network-info",
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
      "name": "chain-data__block__latest",
      "description": "Get latest block. Retrieve the latest block information from Base Mainnet using the public JSON-RPC endpoint. Docs: https://www.brainiac.software/api/chain-data/block-latest",
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
      "name": "chain-data__block__get",
      "description": "Get block by number or hash. Retrieve a specific block by number or hash from Base Mainnet. Supports optional full transaction details. Docs: https://www.brainiac.software/api/chain-data/block-get",
      "parameters": {
        "type": "object",
        "properties": {
          "blockNumber": {
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          },
          "blockHash": {
            "type": "string",
            "pattern": "^0x[0-9a-fA-F]{64}$"
          },
          "fullTransactions": {
            "default": false,
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
      "name": "chain-data__block__transactions",
      "description": "Get block transactions. Retrieve all transactions included in a specific block by number or hash from Base Mainnet. Docs: https://www.brainiac.software/api/chain-data/block-transactions",
      "parameters": {
        "type": "object",
        "properties": {
          "blockNumber": {
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          },
          "blockHash": {
            "type": "string",
            "pattern": "^0x[0-9a-fA-F]{64}$"
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "chain-data__transaction__receipt",
      "description": "Get transaction receipt. Retrieve the receipt and status for a specific transaction on Base Mainnet, including logs and gas used. Docs: https://www.brainiac.software/api/chain-data/transaction-receipt",
      "parameters": {
        "type": "object",
        "properties": {
          "txHash": {
            "type": "string",
            "pattern": "^0x[0-9a-fA-F]{64}$"
          }
        },
        "required": [
          "txHash"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "chain-data__logs__search",
      "description": "Search contract event logs. Search for contract event logs on Base Mainnet with filters for block range, address, and topics. Limited to 1000 results per request. Docs: https://www.brainiac.software/api/chain-data/logs-search",
      "parameters": {
        "type": "object",
        "properties": {
          "fromBlock": {
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          },
          "toBlock": {
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          },
          "blockHash": {
            "type": "string",
            "pattern": "^0x[0-9a-fA-F]{64}$"
          },
          "address": {
            "anyOf": [
              {
                "type": "string",
                "pattern": "^0x[0-9a-fA-F]{40}$"
              },
              {
                "type": "array",
                "items": {
                  "type": "string",
                  "pattern": "^0x[0-9a-fA-F]{40}$"
                }
              }
            ]
          },
          "topics": {
            "default": [],
            "maxItems": 4,
            "type": "array",
            "items": {
              "anyOf": [
                {
                  "type": "string",
                  "pattern": "^0x[0-9a-fA-F]*$"
                },
                {
                  "type": "array",
                  "items": {
                    "type": "string",
                    "pattern": "^0x[0-9a-fA-F]*$"
                  }
                },
                {
                  "type": "null"
                }
              ]
            }
          },
          "limit": {
            "default": 1000,
            "type": "integer",
            "minimum": 1,
            "maximum": 1000
          },
          "cursor": {
            "type": "string",
            "minLength": 1,
            "maxLength": 4000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "chain-data__contract__code",
      "description": "Get contract bytecode. Retrieve the bytecode of a smart contract on Base Mainnet at a specific address and optional block number. Docs: https://www.brainiac.software/api/chain-data/contract-code",
      "parameters": {
        "type": "object",
        "properties": {
          "address": {
            "type": "string",
            "pattern": "^0x[0-9a-fA-F]{40}$"
          },
          "blockNumber": {
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          }
        },
        "required": [
          "address"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "chain-data__contract__read",
      "description": "Execute read-only contract call. Execute a read-only call to a smart contract on Base Mainnet using eth_call. Returns the result without submitting a transaction. Docs: https://www.brainiac.software/api/chain-data/contract-read",
      "parameters": {
        "type": "object",
        "properties": {
          "address": {
            "type": "string",
            "pattern": "^0x[0-9a-fA-F]{40}$"
          },
          "data": {
            "type": "string",
            "pattern": "^0x[0-9a-fA-F]*$"
          },
          "blockNumber": {
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          }
        },
        "required": [
          "address",
          "data"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "chain-data__gas__estimate",
      "description": "Estimate gas for transaction. Estimate the gas required for a transaction on Base Mainnet using eth_estimateGas. Docs: https://www.brainiac.software/api/chain-data/gas-estimate",
      "parameters": {
        "type": "object",
        "properties": {
          "from": {
            "type": "string",
            "pattern": "^0x[0-9a-fA-F]{40}$"
          },
          "to": {
            "type": "string",
            "pattern": "^0x[0-9a-fA-F]{40}$"
          },
          "value": {
            "type": "string",
            "pattern": "^0x[0-9a-fA-F]+$"
          },
          "data": {
            "type": "string",
            "pattern": "^0x[0-9a-fA-F]*$"
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "chain-data__gas__fee-history",
      "description": "Get fee history. Retrieve the fee history for Base Mainnet blocks, including base fees and reward percentiles. Supports EIP-1559. Docs: https://www.brainiac.software/api/chain-data/gas-fee-history",
      "parameters": {
        "type": "object",
        "properties": {
          "blockCount": {
            "default": 100,
            "type": "integer",
            "minimum": 1,
            "maximum": 1024
          },
          "newestBlock": {
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          },
          "rewardPercentiles": {
            "default": [
              25,
              50,
              75
            ],
            "minItems": 1,
            "maxItems": 5,
            "type": "array",
            "items": {
              "type": "number",
              "minimum": 0,
              "maximum": 100
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
      "name": "chain-data__address__native-balance",
      "description": "Get native ETH balance. Retrieve the native ETH balance of a Base Mainnet address from the public JSON-RPC endpoint. Docs: https://www.brainiac.software/api/chain-data/address-native-balance",
      "parameters": {
        "type": "object",
        "properties": {
          "address": {
            "type": "string",
            "pattern": "^0x[a-fA-F0-9]{40}$"
          },
          "blockNumber": {
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          }
        },
        "required": [
          "address"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "chain-data__token__erc20-balance",
      "description": "Get ERC-20 balance. Retrieve the ERC-20 token balance of a wallet for a specified token contract on Base Mainnet using eth_call. Docs: https://www.brainiac.software/api/chain-data/token-erc20-balance",
      "parameters": {
        "type": "object",
        "properties": {
          "walletAddress": {
            "type": "string",
            "pattern": "^0x[a-fA-F0-9]{40}$"
          },
          "tokenAddress": {
            "type": "string",
            "pattern": "^0x[a-fA-F0-9]{40}$"
          },
          "blockNumber": {
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          }
        },
        "required": [
          "walletAddress",
          "tokenAddress"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "chain-data__token__erc20-total-supply",
      "description": "Get ERC-20 total supply. Retrieve the total supply of an ERC-20 token on Base Mainnet using eth_call. Docs: https://www.brainiac.software/api/chain-data/token-erc20-total-supply",
      "parameters": {
        "type": "object",
        "properties": {
          "tokenAddress": {
            "type": "string",
            "pattern": "^0x[a-fA-F0-9]{40}$"
          },
          "blockNumber": {
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          }
        },
        "required": [
          "tokenAddress"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "chain-data__token__metadata",
      "description": "Get token metadata. Retrieve ERC-20 name, symbol, decimals, and total supply for a token on Base Mainnet where supported. Docs: https://www.brainiac.software/api/chain-data/token-metadata",
      "parameters": {
        "type": "object",
        "properties": {
          "tokenAddress": {
            "type": "string",
            "pattern": "^0x[a-fA-F0-9]{40}$"
          },
          "blockNumber": {
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          }
        },
        "required": [
          "tokenAddress"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "chain-data__token__erc20-transfers",
      "description": "Get ERC-20 transfers. Retrieve ERC-20 Transfer events for a token contract or wallet on Base Mainnet over a bounded block range. Docs: https://www.brainiac.software/api/chain-data/token-erc20-transfers",
      "parameters": {
        "type": "object",
        "properties": {
          "tokenAddress": {
            "type": "string",
            "pattern": "^0x[a-fA-F0-9]{40}$"
          },
          "walletAddress": {
            "type": "string",
            "pattern": "^0x[a-fA-F0-9]{40}$"
          },
          "fromBlock": {
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          },
          "toBlock": {
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          },
          "limit": {
            "default": 1000,
            "type": "integer",
            "minimum": 1,
            "maximum": 1000
          },
          "cursor": {
            "type": "string",
            "minLength": 1,
            "maxLength": 4000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "chain-data__address__nonce",
      "description": "Get address nonce. Retrieve the transaction nonce for a Base Mainnet address from the public JSON-RPC endpoint. Docs: https://www.brainiac.software/api/chain-data/address-nonce",
      "parameters": {
        "type": "object",
        "properties": {
          "address": {
            "type": "string",
            "pattern": "^0x[a-fA-F0-9]{40}$"
          },
          "blockNumber": {
            "type": "integer",
            "minimum": 0,
            "maximum": 9007199254740991
          }
        },
        "required": [
          "address"
        ]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "chain-data__gas__current",
      "description": "Base gas oracle current. Current Base gas fees in gwei (base fee plus slow/standard/fast priority from feeHistory percentiles 10/50/90) with a USD estimate for a simple transfer. Snapshot only. Docs: https://www.brainiac.software/api/chain-data/gas-current",
      "parameters": {
        "type": "object",
        "properties": {
          "gasLimit": {
            "type": "integer",
            "minimum": 21000,
            "maximum": 30000000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "chain-data__gas__evm",
      "description": "EVM multi-chain gas oracle. Current EIP-1559 gas snapshot for Ethereum, Base, Arbitrum, Optimism, and Polygon from public RPC, with Chainlink USD estimates for a simple transfer. Docs: https://www.brainiac.software/api/chain-data/gas-evm",
      "parameters": {
        "type": "object",
        "properties": {
          "chain": {
            "type": "string",
            "enum": [
              "ethereum",
              "base",
              "arbitrum",
              "optimism",
              "polygon"
            ]
          },
          "chains": {
            "minItems": 1,
            "maxItems": 5,
            "type": "array",
            "items": {
              "type": "string",
              "enum": [
                "ethereum",
                "base",
                "arbitrum",
                "optimism",
                "polygon"
              ]
            }
          },
          "gasLimit": {
            "type": "integer",
            "minimum": 21000,
            "maximum": 30000000
          }
        },
        "required": []
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "chain-data__ens__resolve",
      "description": "ENS and Basename resolve. Resolve an ENS or Basename to an address, or an address to a forward-confirmed primary name, via official ENS on Ethereum and Basenames on Base. Docs: https://www.brainiac.software/api/chain-data/ens-resolve",
      "parameters": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string",
            "minLength": 3,
            "maxLength": 255
          },
          "address": {
            "type": "string",
            "pattern": "^0x[a-fA-F0-9]{40}$"
          },
          "system": {
            "type": "string",
            "enum": [
              "ens",
              "basename"
            ]
          }
        },
        "required": []
      }
    }
  }
]
TOOL_PRICES: Dict[str, str] = {
  "chain-data__network-info": "0.002",
  "chain-data__block__latest": "0.002",
  "chain-data__block__get": "0.002",
  "chain-data__block__transactions": "0.002",
  "chain-data__transaction__receipt": "0.002",
  "chain-data__logs__search": "0.002",
  "chain-data__contract__code": "0.002",
  "chain-data__contract__read": "0.002",
  "chain-data__gas__estimate": "0.001",
  "chain-data__gas__fee-history": "0.001",
  "chain-data__address__native-balance": "0.002",
  "chain-data__token__erc20-balance": "0.002",
  "chain-data__token__erc20-total-supply": "0.002",
  "chain-data__token__metadata": "0.002",
  "chain-data__token__erc20-transfers": "0.002",
  "chain-data__address__nonce": "0.002",
  "chain-data__gas__current": "0.001",
  "chain-data__gas__evm": "0.001",
  "chain-data__ens__resolve": "0.001"
}
TOOL_ROUTES: Dict[str, str] = {
  "chain-data__network-info": "chain-data/network-info",
  "chain-data__block__latest": "chain-data/block/latest",
  "chain-data__block__get": "chain-data/block/get",
  "chain-data__block__transactions": "chain-data/block/transactions",
  "chain-data__transaction__receipt": "chain-data/transaction/receipt",
  "chain-data__logs__search": "chain-data/logs/search",
  "chain-data__contract__code": "chain-data/contract/code",
  "chain-data__contract__read": "chain-data/contract/read",
  "chain-data__gas__estimate": "chain-data/gas/estimate",
  "chain-data__gas__fee-history": "chain-data/gas/fee-history",
  "chain-data__address__native-balance": "chain-data/address/native-balance",
  "chain-data__token__erc20-balance": "chain-data/token/erc20-balance",
  "chain-data__token__erc20-total-supply": "chain-data/token/erc20-total-supply",
  "chain-data__token__metadata": "chain-data/token/metadata",
  "chain-data__token__erc20-transfers": "chain-data/token/erc20-transfers",
  "chain-data__address__nonce": "chain-data/address/nonce",
  "chain-data__gas__current": "chain-data/gas/current",
  "chain-data__gas__evm": "chain-data/gas/evm",
  "chain-data__ens__resolve": "chain-data/ens/resolve"
}


class BrainiacChainDataAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("HEURIST_PARTNER_KEY") or os.getenv("BRAINIAC_PARTNER_KEY")
        if not self.api_key:
            raise ValueError("HEURIST_PARTNER_KEY (or BRAINIAC_PARTNER_KEY) is required")
        self.base_url = os.getenv("BRAINIAC_PARTNER_ORIGIN", "https://www.brainiac.software").rstrip("/")
        self.metadata.update(
            {
                "name": "BRAINIAC.software — chain-data",
                "version": "1.0.0",
                "author": "BRAINIAC.software",
                "author_address": "0x6428665E83F503904571104311bB78CBb29b975c",
                "description": "Pay-per-call BRAINIAC.software APIs for the chain-data catalog group. Docs: https://www.brainiac.software/how-to-use",
                "external_apis": ["brainiac.software"],
                "tags": ["BRAINIAC", "chain-data", "x402"],
                "image_url": "https://www.brainiac.software/opengraph-image",
                "examples": ["Get network information"],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.001",
                    "tool_prices": TOOL_PRICES,
                },
            }
        )

    def get_system_prompt(self) -> str:
        return (
            "You call BRAINIAC.software paid APIs for the chain-data group. "
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
