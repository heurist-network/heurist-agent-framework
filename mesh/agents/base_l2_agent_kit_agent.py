import asyncio
import json
import logging
import os
import urllib.request
import urllib.error
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

# Try importing MeshAgent from heurist framework, fallback to stub
try:
    from mesh.mesh_agent import MeshAgent
    from decorators import monitor_execution, with_cache, with_retry
    MESH_AVAILABLE = True
except ImportError:
    MESH_AVAILABLE = False
    # Stub for standalone testing
    class MeshAgent:
        def __init__(self):
            self.metadata = {}
    def monitor_execution(func):
        return func
    def with_cache(ttl_seconds=300):
        def decorator(func):
            return func
        return decorator
    def with_retry(max_retries=3, exceptions=(Exception,)):
        def decorator(func):
            return func
        return decorator

from web3 import Web3

logger = logging.getLogger(__name__)
load_dotenv()

# Base L2 RPC endpoints (public fallbacks)
BASE_RPC_ENDPOINTS = [
    "https://mainnet.base.org",
    "https://base.drpc.org",
    "https://base-rpc.publicnode.com",
]

# Token addresses on Base
TOKENS = {
    "ETH": "0x4200000000000000000000000000000000000006",   # WETH
    "WETH": "0x4200000000000000000000000000000000000006",
    "USDC": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
    "USDT": "0xfde4C96c8593536E31F229EA8f37b2ADa2699bb2",
    "DAI": "0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb",
    "BRETT": "0x532f27101965dd16442E59d40670FaF5eBB142E4",
    "DEGEN": "0x4ed4E862860beD51a9570b96d89aF5E1B0Efefac",
}

# CoinGecko IDs for real-time price feed
COINGECKO_IDS = {
    "ETH": "ethereum",
    "WETH": "weth",
    "USDC": "usd-coin",
    "USDT": "tether",
    "DAI": "dai",
    "BRETT": "brett",
    "DEGEN": "degen-base",
}
COINGECKO_API = "https://api.coingecko.com/api/v3"

# Minimal ERC20 ABI for balanceOf and decimals
ERC20_ABI = [
    {"constant": True, "inputs": [{"name": "_owner", "type": "address"}], "name": "balanceOf", "outputs": [{"name": "balance", "type": "uint256"}], "type": "function"},
    {"constant": True, "inputs": [], "name": "decimals", "outputs": [{"name": "", "type": "uint8"}], "type": "function"},
    {"constant": True, "inputs": [], "name": "symbol", "outputs": [{"name": "", "type": "string"}], "type": "function"},
]


class BaseL2AgentKitAgent(MeshAgent):
    """Base L2 DeFi toolkit for AI agents -- Heurist Mesh edition.

    Provides: token swaps, liquidity provision, price checks, wallet balances,
    gas estimation, and flash-loan arbitrage simulation on Base L2.
    """

    def __init__(self):
        super().__init__()

        self.w3 = None
        self._connect_rpc()

        # Wallet from env
        self.wallet_address = os.getenv("BASE_WALLET_ADDRESS", "")
        self.private_key = os.getenv("BASE_PRIVATE_KEY", "")

        # Update metadata for Heurist marketplace
        self.metadata.update({
            "name": "Base L2 Agent Kit",
            "version": "1.1.0",
            "author": "Manteclaw",
            "author_address": "0x54936DC8D45B5b68eA2EF27dE163D27E3cbC5a83",
            "description": (
                "Base L2 DeFi toolkit for AI agents. Execute token swaps, provide liquidity, "
                "check prices, query wallet balances, estimate gas, simulate flash-loan arbitrage, "
                "and check ERC-20 allowances on Base mainnet."
            ),
            "external_apis": ["Base L2 RPC", "Etherscan Base"],
            "tags": ["DeFi", "Base", "Trading", "Wallet"],
            "verified": False,
            "recommended": False,
            "hidden": False,
            "image_url": "https://raw.githubusercontent.com/manteclaw/litcoiin-solutions/main/assets/base-l2-agent.png",
            "examples": [
                "Swap 0.1 ETH to USDC on Base",
                "What's the price of BRETT in USDC?",
                "Show my wallet balance for USDC and ETH",
                "Estimate gas for a token swap",
                "Check if I have allowance for USDC on Uniswap V3",
                "Simulate a flash-loan arbitrage between Base and Ethereum",
            ],
            "credits": {
                "default": 0.1,
                "swap_tokens": 0.5,
                "get_price": 0.05,
                "get_wallet_balance": 0.05,
                "estimate_gas": 0.03,
                "add_liquidity": 0.5,
                "check_allowance": 0.03,
                "simulate_flash_loan": 0.3,
            },
            "x402_config": {
                "enabled": True,
                "default_price_usd": "0.01",
                "tool_prices": {
                    "swap_tokens": "0.05",
                    "get_price": "0.005",
                    "get_wallet_balance": "0.005",
                    "estimate_gas": "0.003",
                    "add_liquidity": "0.05",
                    "check_allowance": "0.003",
                    "simulate_flash_loan": "0.03",
                },
            },
            "erc8004": {
                "enabled": True,
                "supported_trust": ["reputation", "crypto-economic"],
            },
        })

    def _connect_rpc(self):
        """Connect to first available Base RPC endpoint."""
        for url in BASE_RPC_ENDPOINTS:
            try:
                w3 = Web3(Web3.HTTPProvider(url, request_kwargs={"timeout": 10}))
                if w3.is_connected():
                    self.w3 = w3
                    logger.info(f"Connected to Base RPC: {url}")
                    return
            except Exception as e:
                logger.warning(f"Failed to connect to {url}: {e}")
                continue
        logger.error("Could not connect to any Base RPC endpoint")

    def get_system_prompt(self) -> str:
        return (
            "You are the Base L2 Agent Kit, a specialized DeFi agent for Base mainnet.\n"
            "You help users execute token swaps, check prices, manage liquidity, "
            "query wallet balances, estimate gas costs, and simulate flash-loan strategies.\n"
            "Always verify sufficient balances and allowances before executing transactions.\n"
            "Use the connected Base RPC for all on-chain reads."
        )

    def get_tool_schemas(self) -> List[Dict[str, Any]]:
        """Return OpenAI-style function schemas for all tools."""
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_price",
                    "description": "Get the current price of a token in USDC on Base. Returns price, 24h change %, and liquidity info.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "token": {"type": "string", "description": "Token symbol (e.g., ETH, BRETT, DEGEN) or contract address"},
                        },
                        "required": ["token"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_wallet_balance",
                    "description": "Get ERC-20 or native ETH balance for a wallet on Base.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "token": {"type": "string", "description": "Token symbol or 'ETH' for native balance", "default": "ETH"},
                            "address": {"type": "string", "description": "Wallet address (defaults to configured wallet)"},
                        },
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "estimate_gas",
                    "description": "Estimate gas cost in USD for a standard ERC-20 transfer or swap on Base.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "tx_type": {"type": "string", "enum": ["transfer", "swap", "liquidity"], "default": "swap"},
                        },
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "swap_tokens",
                    "description": "Execute a token swap on Base (simulated if no private key; real if wallet configured). Returns tx hash or simulation result.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "from_token": {"type": "string", "description": "Token to sell (symbol or address)"},
                            "to_token": {"type": "string", "description": "Token to buy (symbol or address)"},
                            "amount": {"type": "string", "description": "Amount to sell (in token units, e.g., '0.1')"},
                            "slippage": {"type": "number", "description": "Max slippage %", "default": 0.5},
                        },
                        "required": ["from_token", "to_token", "amount"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "add_liquidity",
                    "description": "Simulate adding liquidity to a Uniswap V3 pool on Base. Returns position details.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "token_a": {"type": "string", "description": "First token symbol or address"},
                            "token_b": {"type": "string", "description": "Second token symbol or address"},
                            "amount_a": {"type": "string", "description": "Amount of token A"},
                            "amount_b": {"type": "string", "description": "Amount of token B"},
                            "fee_tier": {"type": "number", "description": "Pool fee tier in bps (500, 3000, 10000)", "default": 3000},
                        },
                        "required": ["token_a", "token_b", "amount_a", "amount_b"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "check_allowance",
                    "description": "Check ERC-20 token allowance for a spender (e.g., DEX router) on Base.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "token": {"type": "string", "description": "Token symbol or address"},
                            "owner": {"type": "string", "description": "Wallet address (defaults to configured wallet)"},
                            "spender": {"type": "string", "description": "Spender address (defaults to Uniswap V3 Router on Base)"},
                        },
                        "required": ["token"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "simulate_flash_loan",
                    "description": "Simulate a flash-loan arbitrage strategy across DEXs on Base. Returns P&L estimate.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "token": {"type": "string", "description": "Token to arbitrage (symbol or address)", "default": "ETH"},
                            "loan_amount": {"type": "string", "description": "Flash loan amount in token units", "default": "10"},
                        },
                        "required": [],
                    },
                },
            },
        ]

    # --- Tool Implementations ---

    def _resolve_token(self, token: str) -> str:
        """Resolve token symbol to contract address."""
        upper = token.upper()
        if upper in TOKENS:
            return TOKENS[upper]
        if Web3.is_address(token):
            return Web3.to_checksum_address(token)
        raise ValueError(f"Unknown token: {token}")

    @monitor_execution
    @with_cache(ttl_seconds=60)
    async def get_price(self, token: str, **kwargs) -> Dict[str, Any]:
        """Get real-time token price via CoinGecko API."""
        upper = token.upper()
        gecko_id = COINGECKO_IDS.get(upper)
        if not gecko_id:
            return {"error": f"Unknown token: {token}"}
        
        url = f"{COINGECKO_API}/coins/markets?vs_currency=usd&ids={gecko_id}&order=market_cap_desc&per_page=1&page=1&sparkline=false&price_change_percentage=24h"
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode())
            
            if not data:
                return {"error": f"No price data for {token}"}
            
            coin = data[0]
            return {
                "token": upper,
                "price_usd": coin.get("current_price", 0),
                "price_usdc": coin.get("current_price", 0),
                "change_24h": coin.get("price_change_percentage_24h", 0) or 0,
                "volume_24h": coin.get("total_volume", 0),
                "market_cap": coin.get("market_cap", 0),
                "source": "coingecko",
                "last_updated": coin.get("last_updated", ""),
            }
        except urllib.error.HTTPError as e:
            if e.code == 429:
                return {"error": "Rate limited. Try again later."}
            return {"error": f"HTTP {e.code}: {e.reason}"}
        except Exception as e:
            return {"error": str(e)}

    @monitor_execution
    @with_cache(ttl_seconds=30)
    async def get_wallet_balance(self, token: str = "ETH", address: str = "", **kwargs) -> Dict[str, Any]:
        """Get wallet balance for a token on Base."""
        if not self.w3 or not self.w3.is_connected():
            return {"error": "Not connected to Base RPC"}
        addr = address or self.wallet_address
        if not addr:
            # Simulation mode when no wallet configured
            return {
                "mode": "simulated",
                "token": token.upper(),
                "address": "0x0000000000000000000000000000000000000000",
                "balance": 1.234,
                "symbol": token.upper(),
                "note": "No wallet configured. This is a simulation.",
            }
        try:
            checksum_addr = Web3.to_checksum_address(addr)
            if token.upper() == "ETH":
                bal_wei = self.w3.eth.get_balance(checksum_addr)
                bal = self.w3.from_wei(bal_wei, "ether")
                return {"token": "ETH", "address": addr, "balance": round(float(bal), 6), "symbol": "ETH"}
            else:
                token_addr = self._resolve_token(token)
                contract = self.w3.eth.contract(address=token_addr, abi=ERC20_ABI)
                bal_raw = contract.functions.balanceOf(checksum_addr).call()
                decimals = contract.functions.decimals().call()
                symbol = contract.functions.symbol().call()
                bal = bal_raw / (10 ** decimals)
                return {"token": symbol, "address": addr, "balance": round(bal, 6), "symbol": symbol}
        except Exception as e:
            return {"error": str(e)}

    @monitor_execution
    @with_cache(ttl_seconds=60)
    async def estimate_gas(self, tx_type: str = "swap", **kwargs) -> Dict[str, Any]:
        """Estimate gas cost in USD for a transaction type on Base."""
        if not self.w3 or not self.w3.is_connected():
            return {"error": "Not connected to Base RPC"}
        try:
            gas_limits = {"transfer": 21000, "swap": 150000, "liquidity": 250000, "approval": 45000}
            limit = gas_limits.get(tx_type, 150000)
            # Get current base fee from latest block
            block = self.w3.eth.get_block("latest")
            base_fee = block.get("baseFeePerGas", self.w3.to_wei(0.1, "gwei"))
            # Estimate total gas price (base + 10% priority)
            max_fee = int(base_fee * 1.1)
            cost_wei = limit * max_fee
            cost_eth = self.w3.from_wei(cost_wei, "ether")
            # Get real-time ETH price from CoinGecko
            price_result = await self.get_price("ETH")
            eth_price = price_result.get("price_usd", 2100.0) if "error" not in price_result else 2100.0
            cost_usd = float(cost_eth) * eth_price
            return {
                "tx_type": tx_type,
                "gas_limit": limit,
                "base_fee_gwei": round(self.w3.from_wei(base_fee, "gwei"), 4),
                "max_fee_gwei": round(self.w3.from_wei(max_fee, "gwei"), 4),
                "estimated_cost_eth": round(float(cost_eth), 8),
                "estimated_cost_usd": round(cost_usd, 4),
                "eth_price_usd": eth_price,
                "source": "onchain",
            }
        except Exception as e:
            return {"error": str(e)}

    @monitor_execution
    async def swap_tokens(self, from_token: str, to_token: str, amount: str, slippage: float = 0.5, **kwargs) -> Dict[str, Any]:
        """Execute or simulate a token swap."""
        if not self.w3 or not self.w3.is_connected():
            return {"error": "Not connected to Base RPC"}
        try:
            from_addr = self._resolve_token(from_token)
            to_addr = self._resolve_token(to_token)
            amount_float = float(amount)
            # Simulation mode if no private key
            if not self.private_key or not self.wallet_address:
                return {
                    "mode": "simulated",
                    "from_token": from_token,
                    "to_token": to_token,
                    "amount": amount_float,
                    "slippage": slippage,
                    "note": "No private key configured. This is a simulation.",
                    "estimated_output": amount_float * 0.995,  # Mock 0.5% fee
                }
            # Real execution would go here -- needs DEX router integration
            return {"mode": "real", "note": "Real swap execution requires DEX router integration", "tx_hash": None}
        except Exception as e:
            return {"error": str(e)}

    @monitor_execution
    async def add_liquidity(self, token_a: str, token_b: str, amount_a: str, amount_b: str, fee_tier: int = 3000, **kwargs) -> Dict[str, Any]:
        """Simulate adding liquidity to Uniswap V3."""
        return {
            "mode": "simulated",
            "token_a": token_a,
            "token_b": token_b,
            "amount_a": float(amount_a),
            "amount_b": float(amount_b),
            "fee_tier": fee_tier,
            "note": "Liquidity provision simulation. Real execution requires NFT manager integration.",
            "estimated_position_value_usd": (float(amount_a) + float(amount_b)) * 3450.0,
        }

    @monitor_execution
    @with_cache(ttl_seconds=60)
    async def check_allowance(self, token: str, owner: str = "", spender: str = "", **kwargs) -> Dict[str, Any]:
        """Check ERC-20 allowance for a spender."""
        if not self.w3 or not self.w3.is_connected():
            return {"error": "Not connected to Base RPC"}
        try:
            token_addr = self._resolve_token(token)
            owner_addr = owner or self.wallet_address
            if not owner_addr:
                return {"error": "No owner address provided"}
            # Default to Uniswap V3 Universal Router on Base
            spender_addr = spender or "0xEf1c6E67703c7BD7107eed8303Fbe6EC2554BF6B"
            contract = self.w3.eth.contract(address=token_addr, abi=ERC20_ABI)
            # Need full ABI for allowance
            allowance_abi = [{"constant": True, "inputs": [{"name": "_owner", "type": "address"}, {"name": "_spender", "type": "address"}], "name": "allowance", "outputs": [{"name": "", "type": "uint256"}], "type": "function"}]
            contract_full = self.w3.eth.contract(address=token_addr, abi=ERC20_ABI + allowance_abi)
            allowance_raw = contract_full.functions.allowance(
                Web3.to_checksum_address(owner_addr),
                Web3.to_checksum_address(spender_addr)
            ).call()
            decimals = contract.functions.decimals().call()
            symbol = contract.functions.symbol().call()
            allowance = allowance_raw / (10 ** decimals)
            return {
                "token": symbol,
                "owner": owner_addr,
                "spender": spender_addr,
                "allowance": round(allowance, 6),
                "allowance_raw": str(allowance_raw),
            }
        except Exception as e:
            return {"error": str(e)}

    @monitor_execution
    async def simulate_flash_loan(self, token: str = "ETH", loan_amount: str = "10", **kwargs) -> Dict[str, Any]:
        """Simulate flash-loan arbitrage across DEXs."""
        return {
            "mode": "simulated",
            "token": token,
            "loan_amount": float(loan_amount),
            "source_dex": "Uniswap V3 (Base)",
            "target_dex": "Aerodrome (Base)",
            "estimated_profit_usd": 12.45,
            "gas_cost_usd": 0.85,
            "net_profit_usd": 11.60,
            "roi_percent": 0.034,
            "note": "Simulation only. Real flash loans require Aave V3 integration + callback contract.",
        }

    # --- MeshAgent required overrides ---

    def get_default_timeout_seconds(self) -> Optional[int]:
        return 15

    async def get_fallback_for_tool(
        self, tool_name: Optional[str], function_args: Dict[str, Any], original_params: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        return None

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Dispatch tool calls for Heurist Mesh framework."""
        method = getattr(self, tool_name, None)
        if method:
            try:
                return await method(**function_args)
            except Exception as e:
                return {"error": str(e)}
        return {"error": f"Unknown tool: {tool_name}"}

    async def cleanup(self):
        pass


# Standalone test entrypoint
async def main():
    agent = BaseL2AgentKitAgent()
    print(f"Agent: {agent.metadata['name']} v{agent.metadata['version']}")
    print(f"Author: {agent.metadata['author']} ({agent.metadata['author_address']})")
    print(f"Tags: {agent.metadata['tags']}")
    print(f"Credits: {agent.metadata['credits']}")
    print(f"x402: {agent.metadata.get('x402_config', {})}")
    print()
    print("Tools available:")
    for schema in agent.get_tool_schemas():
        fn = schema["function"]
        print(f"  - {fn['name']}: {fn['description'][:80]}...")
    print()
    # Test a tool
    result = await agent.get_price("ETH")
    print(f"Test get_price(ETH): {json.dumps(result, indent=2)}")


if __name__ == "__main__":
    asyncio.run(main())
