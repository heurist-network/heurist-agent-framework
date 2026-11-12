import logging
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode

from decorators import with_cache
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)

API = "https://api.layerhop.com/v1"
SWAP_LINK = "https://layerhop.com/swap"

# Public sample wallets, used only to price an indicative quote when the user gave no address.
# A quote never moves funds; the user signs any swap in their own wallet via the swap link.
SAMPLE_ADDRESS = {
    "evm": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
    "svm": "9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM",
}


class LayerHopSwapQuoteAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.metadata.update(
            {
                "name": "LayerHop Swap Quote Agent",
                "version": "1.0.0",
                "author": "LayerHop",
                "author_address": "0xAA857ee7176bfc34Dd8a792de13934ed9541eD36",
                "description": "Read-only cross-chain and same-chain swap quotes from LayerHop, which compares routes from many bridges and aggregators across 70 chains (Ethereum, Base, Arbitrum, Optimism, BNB Chain, Polygon, Solana, Hyperliquid and more). Returns the best route with the amount received, minimum, fees and ETA, plus a swap link the user opens to review and sign in their own wallet. Never builds or signs transactions.",
                "external_apis": ["LayerHop"],
                "tags": ["DeFi", "Bridge", "Swap", "Cross-chain"],
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/LayerHop.png",
                "examples": [
                    "How much USDC on Arbitrum do I get for 100 USDC on Base?",
                    "Cheapest way to move 0.5 ETH from Ethereum to SOL on Solana",
                    "Quote 250 USDT on BNB Chain to USDC on Base",
                    "Which chains can I bridge to with LayerHop?",
                ],
                "credits": {"default": 1},
            }
        )

    def get_system_prompt(self) -> str:
        return """You help users compare cross-chain and same-chain token swap routes using LayerHop quotes.

- Use get_swap_quote for any "how much would I get" or "cheapest route" question. Amounts are human units ("100" = 100 USDC).
- Present: what the user sends, what they receive and the minimum, total fees, ETA and the provider. Quotes expire in about a minute; say they are estimates, not guarantees.
- If the user gave no wallet address, the quote is indicative; say so.
- To execute, give the swap link: the user reviews and signs in their own wallet. Never ask for or accept private keys or seed phrases. You cannot sign or send transactions.
- Use list_supported_chains when unsure of a chain's slug. Use get_order_status for a swap the user already sent."""

    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_swap_quote",
                    "description": "Best-price quote for swapping or bridging a token between chains (or on one chain). Compares routes from many bridges and aggregators. Returns the amount received, minimum after slippage, fees, ETA, provider, alternatives and a swap link the user signs in their own wallet. Read-only.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "from_chain": {
                                "type": "string",
                                "description": "Source chain slug, e.g. ethereum, base, arbitrum, optimism, bsc, polygon, solana",
                            },
                            "from_token": {
                                "type": "string",
                                "description": "Source token symbol (e.g. USDC, ETH) or contract address",
                            },
                            "amount": {
                                "type": "string",
                                "description": "Amount of the source token in human units, e.g. '100' or '0.5'",
                            },
                            "to_chain": {
                                "type": "string",
                                "description": "Destination chain slug, e.g. arbitrum, solana, hyperliquid",
                            },
                            "to_token": {
                                "type": "string",
                                "description": "Destination token symbol or contract address",
                            },
                            "sender": {
                                "type": "string",
                                "description": "Optional sender wallet address on the source chain. Omit for an indicative quote.",
                            },
                            "recipient": {
                                "type": "string",
                                "description": "Optional recipient address on the destination chain. Defaults to the sender when both chains share a VM.",
                            },
                        },
                        "required": ["from_chain", "from_token", "amount", "to_chain", "to_token"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "list_supported_chains",
                    "description": "List the chains LayerHop routes, with their slugs and VM type.",
                    "parameters": {"type": "object", "properties": {}, "required": []},
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "get_order_status",
                    "description": "Status of a swap the user already sent: pending, filled, refunded or failed.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "provider": {
                                "type": "string",
                                "description": "Provider from the quote, e.g. across, relay, lifi, debridge",
                            },
                            "tx_hash": {"type": "string", "description": "Source-chain transaction hash of the swap"},
                        },
                        "required": ["provider", "tx_hash"],
                    },
                },
            },
        ]

    @with_cache(ttl_seconds=3600)
    async def _chains(self) -> Dict[str, Any]:
        data = await self._api_request(f"{API}/chains")
        if "error" in data:
            return data
        chains = data.get("chains", data) if isinstance(data, dict) else data
        return {"chains": [{"slug": c.get("slug"), "name": c.get("name"), "vm": c.get("vm")} for c in chains]}

    async def _vm(self, slug: str) -> Optional[str]:
        data = await self._chains()
        for c in data.get("chains", []):
            if c.get("slug") == slug:
                return c.get("vm")
        return None

    @with_cache(ttl_seconds=3600)
    async def _token(self, chain: str, token: str) -> Optional[Dict[str, Any]]:
        data = await self._api_request(f"{API}/tokens", params={"chain": chain, "q": token})
        tokens = data.get("tokens", []) if isinstance(data, dict) else []
        want = token.lower()
        for t in tokens:
            if t.get("address", "").lower() == want or t.get("symbol", "").lower() == want:
                return t
        return None

    async def get_swap_quote(
        self,
        from_chain: str,
        from_token: str,
        amount: str,
        to_chain: str,
        to_token: str,
        sender: Optional[str] = None,
        recipient: Optional[str] = None,
    ) -> Dict[str, Any]:
        from_chain, to_chain = from_chain.strip().lower(), to_chain.strip().lower()
        src_vm, dst_vm = await self._vm(from_chain), await self._vm(to_chain)
        if not src_vm or not dst_vm:
            return {
                "error": f"Unknown chain '{from_chain if not src_vm else to_chain}'. Call list_supported_chains for valid slugs."
            }
        src = await self._token(from_chain, from_token.strip())
        dst = await self._token(to_chain, to_token.strip())
        if not src or not dst:
            missing = from_token if not src else to_token
            return {
                "error": f"Token '{missing}' not found on {from_chain if not src else to_chain}. Try its contract address."
            }
        try:
            base_units = int(Decimal(amount) * (Decimal(10) ** int(src["decimals"])))
        except (InvalidOperation, ValueError):
            return {"error": f"Invalid amount '{amount}'. Use a number like '100' or '0.5'."}
        if base_units <= 0:
            return {"error": "Amount must be greater than zero."}

        indicative = sender is None
        sender = sender or SAMPLE_ADDRESS.get(src_vm)
        if recipient is None:
            recipient = sender if src_vm == dst_vm else SAMPLE_ADDRESS.get(dst_vm)
            indicative = indicative or src_vm != dst_vm
        if not sender or not recipient:
            return {"error": "Please provide the sender and recipient wallet addresses for this chain pair."}

        params = {
            "srcChain": from_chain,
            "srcToken": src["address"],
            "amount": str(base_units),
            "dstChain": to_chain,
            "dstToken": dst["address"],
            "sender": sender,
            "recipient": recipient,
        }
        data = await self._api_request(f"{API}/quote", params=params, timeout=20)
        if isinstance(data, dict) and data.get("error"):
            err = data["error"]
            return {"error": err.get("message", str(err)) if isinstance(err, dict) else str(err)}
        best = (data or {}).get("best")
        if not best:
            return {"error": "No route found for this swap."}

        def human(units: str) -> str:
            return str((Decimal(units) / (Decimal(10) ** int(dst["decimals"]))).normalize())

        link = (
            SWAP_LINK
            + "?"
            + urlencode(
                {
                    "srcChain": from_chain,
                    "srcToken": src["symbol"],
                    "dstChain": to_chain,
                    "dstToken": dst["symbol"],
                    "amount": amount,
                }
            )
        )
        alternatives = [
            {
                "provider": q.get("provider"),
                "receive": human(q.get("dstAmount", "0")),
                "eta_seconds": q.get("estimatedSeconds"),
            }
            for q in (data.get("quotes") or [])[1:5]
        ]
        return {
            "send": f"{amount} {src['symbol']} on {from_chain}",
            "receive": f"{human(best['dstAmount'])} {dst['symbol']} on {to_chain}",
            "minimum_received": f"{human(best.get('dstAmountMin', best['dstAmount']))} {dst['symbol']}",
            "provider": best.get("provider"),
            "eta_seconds": best.get("estimatedSeconds"),
            "fees": best.get("fees"),
            "alternatives": alternatives,
            "indicative": indicative,
            "swap_link": link,
            "note": "Quote expires in about a minute. The user reviews and signs in their own wallet via swap_link; this agent never signs or sends transactions.",
        }

    async def get_order_status(self, provider: str, tx_hash: str) -> Dict[str, Any]:
        data = await self._api_request(f"{API}/orders/{provider.strip()}/{tx_hash.strip()}")
        if isinstance(data, dict) and data.get("error"):
            err = data["error"]
            return {"error": err.get("message", str(err)) if isinstance(err, dict) else str(err)}
        return {
            "provider": data.get("provider"),
            "state": data.get("state"),
            "srcTxHash": data.get("srcTxHash"),
            "dstTxHash": data.get("dstTxHash"),
        }

    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        if tool_name == "get_swap_quote":
            return await self.get_swap_quote(**function_args)
        if tool_name == "list_supported_chains":
            return await self._chains()
        if tool_name == "get_order_status":
            return await self.get_order_status(function_args["provider"], function_args["tx_hash"])
        return {"error": f"Unknown tool: {tool_name}"}
