"""
FAST402-ENGINE Base Mainnet DeFi Agent
Provides on-chain DeFi data from Base Mainnet via x402 pay-per-use endpoints.
"""

import logging
import aiohttp
from dotenv import load_dotenv
from mesh.mesh_agent import MeshAgent

load_dotenv()
logger = logging.getLogger(__name__)


class Fast402BaseDeFiAgent(MeshAgent):
    """
    Agent that fetches on-chain DeFi data from Base Mainnet via the FAST402-ENGINE x402 provider.
    Covers wallet assets, portfolio snapshots, token prices, Aerodrome APY, and transaction history.
    """

    def __init__(self):
        super().__init__()
        self.base_url = "https://crypto.fast402.online"  # ← main domain api

    def get_metadata(self):
        return dict(
            name="Fast402BaseDeFiAgent",
            version="1.0.0",
            author="takadevxyz",  # ← username author
            author_address="0xa122360d1b4D0A822f3EF3A66Afb3B846F0ab7D0",  # ← wallet receiver/payto
            description=(
                "Fetches real-time DeFi data from Base Mainnet via FAST402-ENGINE x402 provider. "
                "Supports wallet asset checks, multi-token portfolio snapshots, Uniswap V3 token prices, "
                "Aerodrome gauge APY estimates, and recent USDC transaction history."
            ),
            inputs=[
                {
                    "name": "query",
                    "description": "Natural language query about Base Mainnet DeFi data",
                    "type": "str",
                    "required": False,
                },
                {
                    "name": "tool",
                    "description": "Direct tool call: check_assets | wallet_portfolio | token_price | aerodrome_apy | tx_history",
                    "type": "str",
                    "required": False,
                },
                {
                    "name": "tool_arguments",
                    "description": "Arguments for the direct tool call",
                    "type": "dict",
                    "required": False,
                },
                {
                    "name": "raw_data_only",
                    "description": "If True, return raw tool result without LLM interpretation",
                    "type": "bool",
                    "required": False,
                },
            ],
            outputs=[
                {
                    "name": "response",
                    "description": "DeFi data from Base Mainnet, either LLM-interpreted or raw",
                    "type": "str",
                },
                {
                    "name": "data",
                    "description": "Structured DeFi data from Base Mainnet",
                    "type": "dict",
                },
            ],
            external_apis=["FAST402-ENGINE (Base Mainnet x402 Provider)"],
            tags=["DeFi", "Base", "Aerodrome", "Uniswap", "Wallet", "x402"],
            recommended=True,
            image_url="https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/Base.png",
            examples=[
                "Check ETH balance and USDC balance for wallet 0xabc...123",
                "Get portfolio snapshot for 0xabc...123 including WETH, USDC, AERO",
                "What's the current token price for this Uniswap V3 pool on Base: 0xpool...address",
                "Estimate APY for this Aerodrome gauge: 0xgauge...address",
                "Show recent USDC transactions for wallet 0xabc...123",
            ],
        )

    def get_system_prompt(self) -> str:
        return (
            "You are a Base Mainnet DeFi data assistant powered by FAST402-ENGINE. "
            "You provide accurate, real-time on-chain data from Base Mainnet.\n\n"
            "You have access to these tools:\n"
            "- check_assets: ETH + USDC balance and optional LP reserves for a wallet\n"
            "- wallet_portfolio: Multi-token portfolio snapshot (ETH + ERC20 tokens)\n"
            "- token_price: Real-time price from a Uniswap V3 pool\n"
            "- aerodrome_apy: Estimated APY for an Aerodrome gauge\n"
            "- tx_history: Recent USDC transactions for a wallet\n\n"
            "Always present numbers clearly. For balances, show token symbol and amount. "
            "For APY, note if it's an estimate and what assumptions were made. "
            "For prices, show both directions (token0/token1 and token1/token0). "
            "If a wallet address or pool address looks invalid, say so clearly."
        )

    def get_tool_schemas(self):
        return [
            {
                "type": "function",
                "function": {
                    "name": "check_assets",
                    "description": "Check native ETH balance, USDC balance, and optionally LP reserves for a wallet on Base Mainnet.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "walletAddress": {"type": "string", "description": "Wallet address (0x format)"},
                            "poolAddress": {"type": "string", "description": "Optional LP pool address to fetch reserves"},
                        },
                        "required": ["walletAddress"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "wallet_portfolio",
                    "description": "Get multi-asset portfolio snapshot (ETH + ERC20 tokens) for a wallet on Base Mainnet.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "walletAddress": {"type": "string", "description": "Wallet address (0x format)"},
                            "tokens": {"type": "array", "items": {"type": "string"}, "description": "Optional list of ERC20 addresses"},
                        },
                        "required": ["walletAddress"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "token_price",
                    "description": "Get real-time token price from an Aerodrome Slipstream or vAMM/sAMM pool on Base Mainnet.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "poolAddress": {"type": "string", "description": "Aerodrome or Uniswap V3 pool address (0x format)"},
                        },
                        "required": ["poolAddress"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "aerodrome_apy",
                    "description": "Estimate current APY for an Aerodrome Finance gauge on Base Mainnet.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "gaugeAddress": {"type": "string", "description": "Aerodrome gauge contract address (0x format)"},
                            "lpTokenAddress": {"type": "string", "description": "LP token address associated with the gauge (0x format)"},
                            "rewardTokenPriceUSD": {"type": "number", "description": "Optional USD price of reward token for accurate APY"},
                        },
                        "required": ["gaugeAddress", "lpTokenAddress"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "tx_history",
                    "description": "Fetch recent USDC transaction history for a wallet on Base Mainnet in AI-friendly format.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "walletAddress": {"type": "string", "description": "Wallet address (0x format)"},
                            "limit": {"type": "integer", "description": "Max transactions to return (default: 10, max: 50)"},
                            "startBlock": {"type": "integer", "description": "Optional block number to start scanning from"},
                        },
                        "required": ["walletAddress"],
                    },
                },
            },
        ]
        return [
            {
                "name": "check_assets",
                "description": (
                    "Check native ETH balance, USDC balance, and optionally LP reserves for a wallet on Base Mainnet. "
                    "Use this for basic wallet balance checks."
                ),
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "walletAddress": {
                            "type": "string",
                            "description": "The wallet address to check (0x format)",
                        },
                        "poolAddress": {
                            "type": "string",
                            "description": "Optional LP pool address to fetch reserves",
                        },
                    },
                    "required": ["walletAddress"],
                },
            },
            {
                "name": "wallet_portfolio",
                "description": (
                    "Get a multi-asset portfolio snapshot for a wallet on Base Mainnet. "
                    "Returns ETH balance plus balances for multiple ERC20 tokens. "
                    "Defaults to USDC, DAI, WETH, and AERO if no token list is provided."
                ),
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "walletAddress": {
                            "type": "string",
                            "description": "The wallet address to snapshot (0x format)",
                        },
                        "tokens": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Optional list of ERC20 contract addresses to include",
                        },
                    },
                    "required": ["walletAddress"],
                },
            },
            {
                "name": "token_price",
                "description": (
                    "Get real-time token price from a Uniswap V3 pool on Base Mainnet. "
                    "Returns price in both directions, current tick, liquidity, and fee tier. "
                    "Works with Aerodrome Slipstream (concentrated liquidity) and standard Uniswap V3 pools."
                ),
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "poolAddress": {
                            "type": "string",
                            "description": "Uniswap V3 or Aerodrome Slipstream pool address (0x format)",
                        },
                    },
                    "required": ["poolAddress"],
                },
            },
            {
                "name": "aerodrome_apy",
                "description": (
                    "Estimate the current APY for an Aerodrome Finance gauge on Base Mainnet. "
                    "Returns reward rate, total staked LP, and estimated APY percentage. "
                    "Provide rewardTokenPriceUSD for more accurate APY calculation."
                ),
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "gaugeAddress": {
                            "type": "string",
                            "description": "Aerodrome gauge contract address (0x format)",
                        },
                        "lpTokenAddress": {
                            "type": "string",
                            "description": "LP token address associated with the gauge (0x format)",
                        },
                        "rewardTokenPriceUSD": {
                            "type": "number",
                            "description": "Optional: current USD price of the reward token for accurate APY",
                        },
                    },
                    "required": ["gaugeAddress", "lpTokenAddress"],
                },
            },
            {
                "name": "tx_history",
                "description": (
                    "Fetch recent USDC transaction history for a wallet on Base Mainnet. "
                    "Returns transactions in AI-friendly format with direction (IN/OUT), amounts, and timestamps."
                ),
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "walletAddress": {
                            "type": "string",
                            "description": "The wallet address to fetch transactions for (0x format)",
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Max number of transactions to return (default: 10, max: 50)",
                        },
                        "startBlock": {
                            "type": "integer",
                            "description": "Optional: block number to start scanning from",
                        },
                    },
                    "required": ["walletAddress"],
                },
            },
        ]

    async def _handle_tool_logic(self, tool_name: str, function_args: dict, **kwargs) -> dict:
        endpoint_map = {
            "check_assets": "/v1/base/check-assets",
            "wallet_portfolio": "/v1/base/wallet-portfolio",
            "token_price": "/v1/base/token-price",
            "aerodrome_apy": "/v1/base/aerodrome-apy",
            "tx_history": "/v1/base/tx-history",
        }

        if tool_name not in endpoint_map:
            return {"error": f"Unknown tool: {tool_name}"}

        url = f"{self.base_url}{endpoint_map[tool_name]}"

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=function_args) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 402:
                    return {
                        "error": "Payment required",
                        "details": "This endpoint requires x402 payment. Configure payment middleware.",
                    }
                else:
                    error_body = await response.text()
                    return {
                        "error": f"Request failed with status {response.status}",
                        "details": error_body,
                    }

    async def _run_tool(self, tool_name: str, tool_arguments: dict, **kwargs) -> dict:
        return await self._handle_tool_logic(tool_name, tool_arguments, **kwargs)


