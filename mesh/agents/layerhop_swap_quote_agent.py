import logging
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode

import aiohttp

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

    async def _get(self, path: str, params: Optional[Dict[str, str]] = None, timeout: int = 20) -> Dict[str, Any]:
        """GET a LayerHop endpoint. Keeps the API's JSON error body ({"error": {"code", "message"}}) on 4xx/5xx."""
        if not self.session:
            self.session = aiohttp.ClientSession()
        try:
            async with self.session.get(
                f"{API}{path}", params=params, timeout=aiohttp.ClientTimeout(total=timeout)
            ) as response:
                try:
                    data = await response.json(content_type=None)
                except Exception:
                    data = None
                if response.status >= 400:
                    err = data.get("error") if isinstance(data, dict) else None
                    if isinstance(err, dict):
                        msg = err.get("message") or err.get("code") or str(err)
                        hints = (err.get("details") or {}).get("suggestions")
                        return {"error": f"{msg} Suggestions: {hints}" if hints else msg}
                    return {"error": str(err) if err else f"LayerHop API returned HTTP {response.status}"}
                return data if isinstance(data, dict) else {"data": data}
        except Exception as e:
            logger.error(f"LayerHop request failed: {e}")
            return {"error": f"LayerHop API request failed: {e}"}

    @with_cache(ttl_seconds=3600)
    async def _chains(self) -> Dict[str, Any]:
        data = await self._get("/chains")
        if "error" in data:
            return data
        chains = data.get("chains", data.get("data", []))
        return {"chains": [{"slug": c.get("slug"), "name": c.get("name"), "vm": c.get("vm")} for c in chains]}

    async def _vm(self, slug: str) -> Optional[str]:
        data = await self._chains()
        for c in data.get("chains", []):
            if c.get("slug") == slug:
                return c.get("vm")
        return None

    @with_cache(ttl_seconds=3600)
    async def _token(self, chain: str, token: str) -> Dict[str, Any]:
        """Resolve a symbol or contract address to one token: {"token": {...}} or {"error": ...} (errors are not cached)."""
        data = await self._get("/tokens", params={"chain": chain, "q": token})
        if "error" in data:
            return data
        tokens = data.get("tokens", [])
        want = token.lower()
        by_address = [t for t in tokens if t.get("address", "").lower() == want]
        if by_address:
            return {"token": by_address[0]}
        same_symbol = [t for t in tokens if t.get("symbol", "").lower() == want]
        # Never pick among look-alikes: take the one verified, popular token, else ask for the address.
        for pool in (
            [t for t in same_symbol if t.get("verified") and t.get("popular")],
            [t for t in same_symbol if t.get("verified")],
        ):
            if len(pool) == 1:
                return {"token": pool[0]}
            if len(pool) > 1:
                break
        if not same_symbol:
            return {"error": f"Token '{token}' not found on {chain}. Try its contract address."}
        options = ", ".join(f"{t.get('name')} ({t.get('address')})" for t in same_symbol[:5])
        return {"error": f"More than one '{token}' on {chain}: {options}. Ask the user which contract address to use."}

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
        src_res = await self._token(from_chain, from_token.strip())
        if "error" in src_res:
            return src_res
        dst_res = await self._token(to_chain, to_token.strip())
        if "error" in dst_res:
            return dst_res
        src, dst = src_res["token"], dst_res["token"]
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
        data = await self._get("/quote", params=params, timeout=20)
        if "error" in data:
            return data
        best = data.get("best")
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
                    "srcToken": src["address"],
                    "dstChain": to_chain,
                    "dstToken": dst["address"],
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
        data = await self._get(f"/orders/{provider.strip()}/{tx_hash.strip()}")
        if "error" in data:
            return data
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
