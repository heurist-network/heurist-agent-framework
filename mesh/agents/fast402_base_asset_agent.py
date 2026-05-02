import httpx
from typing import Any

from mesh.mesh_agent import MeshAgent


class Fast402BaseAssetAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.metadata.update(
            {
                "name": "Fast402 Base Asset Agent",
                "version": "1.0.0",
                "author": "fast402",                                    # ganti nama lo
                "author_address": "0xa122360d1b4D0A822f3EF3A66Afb3B846F0ab7D0",
                "description": (
                    "Check native ETH balance and Uniswap/Aerodrome liquidity pool "
                    "reserves on Base Mainnet for any wallet address. "
                    "Data is fetched in real-time from the Base blockchain via the "
                    "Fast402 engine. Use when you need on-chain balance data or "
                    "LP reserve snapshots on Base."
                ),
                "external_apis": ["crypto.fast402.online"],
                "tags": ["Base", "DeFi", "Wallet", "Blockchain", "ETH", "LP"],
                "image_url": "https://crypto.fast402.online/favicon.png",  # opsional
                "examples": [
                    "Check ETH balance of 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
                    "Get LP reserves for Aerodrome pool 0x7f670f78B17dEC44d5Ef68a48740b6f8849cc2e6",
                    "What is the ETH balance of vitalik.eth on Base?",
                ],
            }
        )

    def get_system_prompt(self) -> str:
        return """
        You are a Base Network data agent powered by the Fast402 engine.

        You can:
        1. Check the native ETH balance of any wallet address on Base Mainnet
        2. Fetch reserve data (reserve0, reserve1) from any Uniswap V2-compatible
           or Aerodrome liquidity pool on Base Mainnet

        Always return structured data. When a wallet address is provided,
        always include the ETH balance. When a pool address is also provided,
        include the LP reserve data alongside the wallet balance.

        Data is fetched in real-time from the Base blockchain.
        Price per call: $0.1 USDC.
        """

    def get_tool_schemas(self) -> list[dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "check_base_assets",
                    "description": (
                        "Check native ETH balance and optionally liquidity pool reserves "
                        "for a wallet on Base Mainnet. Returns real-time on-chain data."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "wallet_address": {
                                "type": "string",
                                "description": "Ethereum wallet address (0x...) to check on Base Mainnet",
                            },
                            "pool_address": {
                                "type": "string",
                                "description": (
                                    "Optional: Uniswap V2 / Aerodrome liquidity pool "
                                    "contract address on Base Mainnet to fetch reserves"
                                ),
                            },
                        },
                        "required": ["wallet_address"],
                    },
                },
            }
        ]

    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: dict | None = None
    ) -> dict[str, Any]:
        if tool_name != "check_base_assets":
            return {"error": f"Unknown tool: {tool_name}"}

        wallet_address = function_args.get("wallet_address", "").strip()
        pool_address = function_args.get("pool_address", "").strip()

        if not wallet_address:
            return {"error": "wallet_address is required"}

        if not wallet_address.startswith("0x") or len(wallet_address) != 42:
            return {"error": f"Invalid wallet address format: {wallet_address}"}

        # Build request payload
        payload: dict[str, str] = {"walletAddress": wallet_address}
        if pool_address:
            if not pool_address.startswith("0x") or len(pool_address) != 42:
                return {"error": f"Invalid pool address format: {pool_address}"}
            payload["poolAddress"] = pool_address

        # Call Fast402 server — x402 payment handled server-side
        # The server returns 402 for unpaid requests, 200 for paid ones.
        # Since this is a Heurist Mesh wrapper, we call directly (no x402 client).
        # Heurist handles billing separately via their own payment layer.
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(
                    "https://crypto.fast402.online/v1/base/check-assets",
                    json=payload,
                    headers={"Content-Type": "application/json"},
                )
        except httpx.TimeoutException:
            return {"error": "Request timed out after 30s"}
        except httpx.RequestError as exc:
            return {"error": f"Network error: {str(exc)}"}

        if response.status_code == 402:
            return {
                "error": "Payment required — Fast402 server returned 402",
                "hint": "This is expected if calling without x402 payment. Heurist will handle billing.",
            }

        if response.status_code != 200:
            return {
                "error": f"Provider error HTTP {response.status_code}",
                "detail": response.text[:300],
            }

        try:
            data = response.json()
        except Exception:
            return {"error": "Invalid JSON response from provider"}

        # Normalize output
        result: dict[str, Any] = {
            "network": data.get("network", "Base Mainnet"),
            "wallet": wallet_address,
            "native_eth_balance": data.get("data", {}).get("native_eth", "unknown"),
            "timestamp": data.get("data", {}).get("timestamp"),
        }

        lp = data.get("data", {}).get("liquidity_pool")
        if isinstance(lp, dict):
            result["liquidity_pool"] = {
                "pool_address": pool_address,
                "reserve0": lp.get("reserve0"),
                "reserve1": lp.get("reserve1"),
            }
        else:
            result["liquidity_pool"] = None

        return {"status": "success", "data": result}