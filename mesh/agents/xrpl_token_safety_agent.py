import re
import time
from urllib.parse import urlencode

from decorators import with_cache, with_retry
from mesh.mesh_agent import MeshAgent


class XrplTokenSafetyAgent(MeshAgent):
    """Read dated public token snapshots; never purchase a report or sign a transaction."""

    CATALOG = "https://cocoeatsai.com/area4/token/catalog.json"

    def __init__(self):
        super().__init__()
        self.metadata.update({
            "name": "XRPL Token Safety",
            "version": "1.0.0",
            "author": "Zach Riehn / Launch Lab",
            "author_address": "0x6fE6079cDAe9199b1aCE8E89b11A687636E7b895",
            "description": "Look up dated XRPL token checks by exact issuer and currency. Returns the published score, up to three flags, source time and links. Limited to the public snapshot catalog; not a safety guarantee.",
            "external_apis": ["Launch Lab public token catalog"],
            "tags": ["XRPL", "Token Safety"],
            "verified": False,
            "image_url": "https://cocoeatsai.com/area4/token/rlusd-rMxCKbED-a364197ffb/og.png",
            "examples": ["Check RLUSD issued by rMxCKbEDwqr76QuheSUMdEGf4B9xJ8m5De"],
            "x402_config": {"enabled": True, "default_price_usd": "0.003"},
        })

    def get_system_prompt(self):
        return (
            "Report the exact issuer, currency and snapshot date. Higher published scores mean fewer detected "
            "risk flags, not guaranteed safety. Disclose stale data and limited catalog coverage. Never infer "
            "identity from a ticker alone. The optional full report costs 5 XRP; only provide its link, never pay."
        )

    def get_tool_schemas(self):
        return [{"type": "function", "function": {
            "name": "check_token_safety",
            "description": "Find a dated public XRPL token snapshot by exact issuer and currency, with score and up to three published flags. No live ledger query or payment.",
            "parameters": {"type": "object", "properties": {
                "issuer": {"type": "string", "description": "Exact classic XRPL issuer address, case-sensitive."},
                "currency": {"type": "string", "description": "Exact case-sensitive currency code (e.g. RLUSD) or its 40-character hexadecimal encoding."},
            }, "required": ["issuer", "currency"]},
        }}]

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=2)
    async def _catalog(self):
        result = await self._api_request(self.CATALOG, timeout=10)
        if "error" in result:
            raise RuntimeError(result["error"])
        return result

    async def _handle_tool_logic(self, tool_name, function_args, session_context=None):
        if tool_name != "check_token_safety":
            return {"error": f"Unsupported tool: {tool_name}"}
        issuer = function_args.get("issuer", "")
        currency = function_args.get("currency", "")
        if not re.fullmatch(r"r[1-9A-HJ-NP-Za-km-z]{24,34}", issuer):
            return {"error": "Provide a classic XRPL issuer address."}
        if re.fullmatch(r"[0-9A-Fa-f]{40}", currency):
            currency = currency.upper()
        elif re.fullmatch(r"[A-Za-z0-9?!@#$%^&*<>(){}\[\]|]{3,20}", currency):
            if len(currency) != 3:
                currency = currency.encode("ascii").hex().upper().ljust(40, "0")
        else:
            return {"error": "Provide a 3–20 character currency code or 40-character hexadecimal currency."}
        for token in await self._catalog():
            if token["issuer"] == issuer and token["currency"] == currency:
                return {
                    "issuer": issuer, "currency": currency, "score": token["score"],
                    "score_scale": "0–100; higher means fewer detected flags, not guaranteed safety",
                    "flags": token["flags"][:3], "as_of": token["as_of"],
                    "stale": time.time() - token["as_of"] > 86400,
                    "stale_after_seconds": 86400,
                    "token_page_url": f"https://cocoeatsai.com/area4/token/{token['slug']}/",
                    "report_url": "https://cocoeatsai.com/area4/report/?" + urlencode({"issuer": issuer, "currency": currency}),
                    "report_price_xrp": "5",
                    "note": "Dated automated checks, not an audit, endorsement or guarantee. No purchase performed.",
                }
        return {"error": "Token not in the public snapshot catalog; this says nothing about its safety."}
