import json
import logging
import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from decorators import with_retry
from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)

# -----------------------------
# Basic validators & utilities
# -----------------------------
EVM_ADDR_RE = re.compile(r"^0x[a-fA-F0-9]{40}$")
SOLANA_B58_RE = re.compile(r"^[1-9A-HJ-NP-Za-km-z]{32,44}$")

ALLOWED_CHAINS = {
    "ethereum",
    "base",
    "arbitrum",
    "optimism",
    "bsc",
    "polygon",
    "avalanche",
    "fantom",
    "solana",
    "tron",
    "linea",
    "blast",
    "zksync",
    "scroll",
    "celo",
    "moonriver",
    "moonbeam",
}


COINGECKO_TO_DEXSCREENER_PLATFORM = {
    "binance-smart-chain": "bsc",
    "arbitrum-one": "arbitrum",
    "optimistic-ethereum": "optimism",
    "polygon-pos": "polygon",
    "sei-network": "sei",
    "zora-network": "zora",
    "blast-mainnet": "blast",
}

YF_DEFAULT_INTERVAL = "1d"
YF_DEFAULT_PERIOD = "6mo"

# Minimum 24h volume threshold for DEX pools (filters out low-activity/fake pools)
MIN_POOL_VOLUME_24H = 3000


def _is_evm_address(s: str) -> bool:
    return bool(EVM_ADDR_RE.match(s or ""))


def _is_solana_address(s: str) -> bool:
    return bool(SOLANA_B58_RE.match(s or ""))


def _normalize_chain(chain: Optional[str]) -> Optional[str]:
    if not chain:
        return None
    c = chain.strip().lower()
    if c in ALLOWED_CHAINS:
        return c
    if c in {"eth", "mainnet"}:
        return "ethereum"
    if c in {"bsc", "binance-smart-chain", "bnb-chain"}:
        return "bsc"
    return c


def _normalize_platform_name(platform_id: str) -> str:
    return COINGECKO_TO_DEXSCREENER_PLATFORM.get(platform_id, platform_id)


def _safe_float(x) -> Optional[float]:
    try:
        return float(x)
    except Exception:
        return None


def _uniq(seq: List[Any]) -> List[Any]:
    seen = set()
    out = []
    for item in seq:
        k = json.dumps(item, sort_keys=True) if isinstance(item, (dict, list)) else str(item)
        if k not in seen:
            seen.add(k)
            out.append(item)
    return out


def _clean_empty_fields(obj: Any) -> Any:
    """Recursively remove empty fields (None, [], {}) from objects"""
    if isinstance(obj, dict):
        cleaned = {}
        for key, value in obj.items():
            cleaned_value = _clean_empty_fields(value)
            # Only include non-empty values
            if cleaned_value is not None and cleaned_value != [] and cleaned_value != {}:
                cleaned[key] = cleaned_value
        return cleaned
    elif isinstance(obj, list):
        cleaned_list = []
        for item in obj:
            cleaned_item = _clean_empty_fields(item)
            if cleaned_item is not None and cleaned_item != [] and cleaned_item != {}:
                cleaned_list.append(cleaned_item)
        return cleaned_list
    else:
        return obj


def _is_same_symbol_pair(pair: Dict[str, Any]) -> bool:
    """Check if a pair has the same symbol for both base and quote tokens (invalid pair)"""
    base = pair.get("baseToken") or {}
    quote = pair.get("quoteToken") or {}
    base_symbol = base.get("symbol", "").upper()
    quote_symbol = quote.get("symbol", "").upper()
    return bool(base_symbol and quote_symbol and base_symbol == quote_symbol)


def _has_sufficient_volume(pair: Dict[str, Any]) -> bool:
    """Check if a pair has sufficient 24h volume to be considered active.
    Returns True if volume data is not available (benefit of the doubt).
    """
    volume_obj = pair.get("volume")
    if not volume_obj:
        return True  # No volume data available, don't filter

    volume_24h = volume_obj.get("h24")
    if volume_24h is None:
        return True  # No 24h volume data, don't filter

    return volume_24h >= MIN_POOL_VOLUME_24H


def _extract_links_from_preview(preview: Dict[str, Any]) -> Dict[str, List]:
    """Extract standardized links structure from pair preview"""
    return {
        "website": preview.get("websites") or [],
        "twitter": [s.get("url") for s in preview.get("socials", []) if (s or {}).get("type") == "twitter"],
        "telegram": [s.get("url") for s in preview.get("socials", []) if (s or {}).get("type") == "telegram"],
    }


# -----------------------------
# Agent
# -----------------------------
class TokenResolverAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.metadata.update(
            {
                "name": "Token Resolver Agent",
                "version": "1.1.0",
                "author": "Heurist team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "Find tokens by address/symbol/name/CoinGecko ID, return normalized profiles and top DEX pools. Pulls extra context (sites/socials/funding/indicators) where available.",
                "external_apis": [
                    "CoinGecko",
                    "DexScreener",
                    "Bitquery (Solana)",
                    "GMGN/Unifai",
                    "Yahoo Finance (optional)",
                    "Coinsider (optional)",
                ],
                "tags": ["Token Search", "Market Data", "x402"],
                "recommended": True,
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/token-resolver-agent.png",
                "examples": [
                    "search query=ETH",
                    "search query=0xEF22cb48B8483dF6152e1423b19dF5553BbD818b chain=base",
                    "profile chain=base address=0xEF22cb48B8483dF6152e1423b19dF5553BbD818b include=['pairs']",
                    "profile symbol=BTC include=['funding_rates','technical_indicators']",
                ],
                "x402_config": {
                    "enabled": True,
                    "default_price_usd": "0.01",
                },
            }
        )

    # -----------------------------
    # System prompt
    # -----------------------------
    def get_system_prompt(self) -> str:
        return (
            "You resolve crypto tokens. Be precise. Detect addresses (EVM/Solana), tickers, exact names, and CoinGecko IDs. "
            "Return compact, normalized objects; include high-signal fields (websites/socials when present). "
            "Not supporting vague keywords. No pagination. No confidence scores. "
            "Do not treat missing DEX pools as an error (CEX-only assets are valid)."
        )

    # -----------------------------
    # Tool schemas (no dots in names)
    # -----------------------------
    def get_tool_schemas(self) -> List[Dict]:
        return [
            {
                "type": "function",
                "function": {
                    "name": "search",
                    "description": "Find tokens by address, ticker/symbol, or token name. Returns up to 5 concise candidates with basic market/trading context. Use this tool for searching new tokens, unfamiliar tokens, or ambiguous queries. Do not search for multiple assets with one search query. This tool may return multiple assets with the same or similar name/symbol, and in this case you should identify the asset with largest market cap / volume or liquidity to identify the probable asset and ignore the others. The result might include scam tokens (indicated by higher-than-usual market cap with very low volume), which is totally normal and you should ignore them without reporting as errors.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "0x… (EVM), Solana mint, ticker/symbol or token name",
                            },
                            "chain": {
                                "type": "string",
                                "description": "Optional chain hint (e.g., base, ethereum, solana). ONLY use this field if you have direct context mentioning the chain. Leave this field blank otherwise.",
                            },
                            "type_hint": {
                                "type": "string",
                                "enum": ["address", "symbol", "name"],
                                "description": "Optional explicit hint for the type of the query",
                            },
                        },
                        "required": ["query"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "profile",
                    "description": "Get detailed profile and market data of a token. Identify it by ONE OF: chain+address (for contract tokens) or symbol (for native/well-known tokens) or coingecko_id. Optional sections to return: pairs, holders (Solana only), traders (Solana only), funding_rates (Binance-listed large caps only), technical_indicators (large caps only). Use this tool for well-known tokens such as BTC, ETH, SOL, or for tokens that you already know its chain+address or Coingecko ID. Prefer to use Coingecko ID if available. If the token is not well-known, use search tool first to get the disambiguated token information. Only enable pairs section if the token is an altcoin or you believe it has a DEX pool (some tokens are only traded on CEXs). Do not enable pairs section for large caps tokens",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "chain": {
                                "type": "string",
                                "description": "Blockchain network (e.g., ethereum, base, bsc, solana)",
                            },
                            "address": {
                                "type": "string",
                                "description": "Token contract address (use with chain parameter)",
                            },
                            "symbol": {
                                "type": "string",
                                "description": "Ticker symbol like BTC or ETH. Only use this for well-known native tokens.",
                            },
                            "coingecko_id": {"type": "string"},
                            "include": {
                                "type": "array",
                                "items": {
                                    "type": "string",
                                    "enum": [
                                        "pairs",
                                        "holders",
                                        "traders",
                                        "funding_rates",
                                        "technical_indicators",
                                    ],
                                },
                                "default": ["pairs"],
                            },
                            "top_n_pairs": {"type": "integer", "default": 3, "minimum": 1, "maximum": 10},
                            "indicator_interval": {"type": "string", "enum": ["1h", "1d"], "default": "1d"},
                        },
                        "required": [],
                    },
                },
            },
        ]

    # -----------------------------
    # Bridge to other Mesh agents (cached 300s)
    # -----------------------------
    async def _cg_get_token_info(self, query_or_id: str) -> Dict[str, Any]:
        try:
            return await self._call_agent_tool(
                "mesh.agents.coingecko_token_info_agent",
                "CoinGeckoTokenInfoAgent",
                "get_token_info",
                {"coingecko_id": query_or_id},
            )
        except Exception as e:
            logger.warning(f"CoinGecko agent failed for {query_or_id}: {e}")
            return {"status": "error", "error": f"CoinGecko lookup failed: {e}"}

    async def _ds_search_pairs(self, search_term: str) -> Dict[str, Any]:
        try:
            return await self._call_agent_tool(
                "mesh.agents.dexscreener_token_info_agent",
                "DexScreenerTokenInfoAgent",
                "search_pairs",
                {"search_term": search_term},
            )
        except Exception as e:
            logger.warning(f"DexScreener search_pairs failed for {search_term}: {e}")
            return {"status": "error", "error": f"DexScreener search failed: {e}"}

    async def _ds_token_pairs(self, chain: Optional[str], token_address: str) -> Dict[str, Any]:
        try:
            return await self._call_agent_tool(
                "mesh.agents.dexscreener_token_info_agent",
                "DexScreenerTokenInfoAgent",
                "get_token_pairs",
                {"chain": chain or "all", "token_address": token_address},
            )
        except Exception as e:
            logger.warning(f"DexScreener get_token_pairs failed for {chain}:{token_address}: {e}")
            return {"status": "error", "error": f"DexScreener token pairs failed: {e}"}

    async def _gmgn_token_info(self, chain: str, address: str) -> Dict[str, Any]:
        try:
            return await self._call_agent_tool(
                "mesh.agents.unifai_token_analysis_agent",
                "UnifaiTokenAnalysisAgent",
                "get_gmgn_token_info",
                {"chain": chain, "address": address},
            )
        except Exception as e:
            logger.info(f"[token_resolver] GMGN unavailable: {e}")
            return {"status": "no_data", "error": "gmgn_unavailable"}

    async def _bq_solana_holders(self, mint: str, limit: int = 5) -> Dict[str, Any]:
        try:
            return await self._call_agent_tool(
                "mesh.agents.bitquery_solana_token_info_agent",
                "BitquerySolanaTokenInfoAgent",
                "query_token_holders",
                {"token_address": mint, "limit": limit},
            )
        except Exception as e:
            logger.info(f"[token_resolver] Bitquery holders unavailable: {e}")
            return {"status": "no_data", "error": "bitquery_unavailable"}

    async def _bq_solana_traders(self, mint: str, limit: int = 5) -> Dict[str, Any]:
        try:
            return await self._call_agent_tool(
                "mesh.agents.bitquery_solana_token_info_agent",
                "BitquerySolanaTokenInfoAgent",
                "query_top_traders",
                {"token_address": mint, "limit": limit},
            )
        except Exception as e:
            logger.info(f"[token_resolver] Bitquery traders unavailable: {e}")
            return {"status": "no_data", "error": "bitquery_unavailable"}

    async def _funding_rates(self, symbol: str) -> Dict[str, Any]:
        try:
            return await self._call_agent_tool(
                "mesh.agents.funding_rate_agent",
                "FundingRateAgent",
                "get_symbol_oi_and_funding",
                {"symbol": symbol},
            )
        except Exception as e:
            logger.info(f"[token_resolver] Funding rates unavailable: {e}")
            return {"status": "no_data", "error": "funding_unavailable"}

    async def _yahoo_indicator_snapshot(
        self, yf_symbol: str, interval: str = YF_DEFAULT_INTERVAL, period: str = YF_DEFAULT_PERIOD
    ) -> Dict[str, Any]:
        try:
            return await self._call_agent_tool(
                "mesh.agents.yahoo_finance_agent",
                "YahooFinanceAgent",
                "indicator_snapshot",
                {"symbol": yf_symbol, "interval": interval, "period": period},
            )
        except Exception as e:
            logger.info(f"[token_resolver] Yahoo indicators unavailable: {e}")
            return {"status": "no_data", "error": "yahoo_unavailable"}

    # -----------------------------
    # Transform helpers
    # -----------------------------
    def _detect_query_type(self, query: str, type_hint: Optional[str]) -> str:
        if type_hint in {"address", "symbol", "name", "coingecko_id"}:
            return type_hint
        q = (query or "").strip()

        # Long strings are likely addresses
        if len(q) >= 20:
            if _is_evm_address(q) or _is_solana_address(q):
                return "address"
            # Could be a long address we don't recognize, try as address anyway
            return "address"

        # Short alphanumeric strings without spaces - treat as symbol
        if re.fullmatch(r"[A-Za-z0-9\-]{2,20}", q) and " " not in q:
            return "symbol"

        # Lowercase with hyphens - likely coingecko_id
        if re.fullmatch(r"[a-z0-9\-]{2,64}", q) and "-" in q:
            return "coingecko_id"

        # Multi-word strings - treat as name
        if " " in q and len(q.strip()) >= 3:
            return "name"

        # Default to symbol for short strings (covers mixed case like "Aster")
        if len(q) >= 2:
            return "symbol"

        return "unknown"

    def _pair_to_preview(self, p: Dict[str, Any]) -> Dict[str, Any]:
        vol = (p.get("volume") or {}).get("h24")
        liq = (p.get("liquidity") or {}).get("usd")
        info = p.get("info") or {}
        chain = p.get("chainId")
        pair_address = p.get("pairAddress")
        link = f"https://dexscreener.com/{chain}/{pair_address.lower()}"
        return {
            "link": link,
            "dex": p.get("dexId"),
            "price_usd": _safe_float(p.get("priceUsd")),
            "volume24h_usd": _safe_float(vol),
            "liquidity_usd": _safe_float(liq),
            "txns24h": (p.get("txns") or {}).get("h24"),
            "websites": info.get("websites") or [],
            "socials": info.get("socials") or [],
        }

    def _extract_token_from_pair(self, pair: Dict[str, Any], prefer_base: bool = True) -> Tuple[Dict[str, Any], str]:
        base = pair.get("baseToken") or {}
        quote = pair.get("quoteToken") or {}
        stables = {"USDC", "USDT", "DAI", "USDe", "FDUSD", "TUSD", "USDJ", "USDD"}
        chosen = base if prefer_base else quote
        other = quote if prefer_base else base
        if (chosen.get("symbol", "").upper() in stables) and (other.get("symbol", "").upper() not in stables):
            chosen = other
        chain = pair.get("chainId")
        tok = {
            "address": chosen.get("address", "").lower() if chosen.get("address") else None,
            "name": chosen.get("name"),
            "symbol": chosen.get("symbol"),
            "chain": chain,
        }
        return tok, chain

    def _merge_links(self, current: Dict[str, Any], add: Dict[str, Any]) -> Dict[str, Any]:
        out = dict(current or {})
        if not add:
            return out

        # normalize to arrays where appropriate
        def _as_list(x):
            if x is None:
                return []
            if isinstance(x, list):
                return [v for v in x if v]
            return [x]

        out["website"] = _uniq(_as_list(out.get("website")) + _as_list(add.get("website")))
        out["twitter"] = _uniq(_as_list(out.get("twitter")) + _as_list(add.get("twitter")))
        out["telegram"] = _uniq(_as_list(out.get("telegram")) + _as_list(add.get("telegram")))
        out["github"] = _uniq(_as_list(out.get("github")) + _as_list(add.get("github")))
        out["explorers"] = _uniq(_as_list(out.get("explorers")) + _as_list(add.get("explorers")))
        return out

    # -----------------------------
    # Core operations
    # -----------------------------
    async def _enrich_with_profile_data(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Enrich search result with profile data when coingecko_id is available"""
        cgid = result.get("coingecko_id")
        if not cgid:
            return result

        profile_result = await self._profile(
            chain=None,
            address=None,
            symbol=None,
            coingecko_id=cgid,
            include=["technical_indicators"],
            top_n_pairs=0,
            indicator_interval="1d",
        )

        if profile_result.get("status") == "success":
            result["profile"] = profile_result.get("data", {})

        return result

    @with_retry(max_retries=2)
    async def _search(self, query: str, chain: Optional[str], qtype: str, limit: int) -> Dict[str, Any]:
        chain = _normalize_chain(chain)
        results: List[Dict[str, Any]] = []

        if qtype == "unknown":
            # Fallback: treat as symbol for backwards compatibility
            qtype = "symbol"

        if qtype == "address":
            pairs_res = await self._ds_token_pairs(chain or "all", query)
            pairs = ((pairs_res or {}).get("data") or {}).get("pairs") or []
            if not pairs:
                if chain:
                    results.append(
                        {
                            "name": None,
                            "symbol": None,
                            "chain": chain,
                            "address": query.lower(),
                            "coingecko_id": None,
                            "price_usd": None,
                            "market_cap_usd": None,
                            "top_pairs": [],
                            "links": {},
                        }
                    )
                return {"status": "success", "data": {"results": results, "timestamp": datetime.utcnow().isoformat()}}

            best_by_token: Dict[str, Dict[str, Any]] = {}
            for p in pairs:
                if _is_same_symbol_pair(p):
                    logger.debug(
                        f"[token_resolver] Skipping invalid same-symbol pair: "
                        f"{p.get('baseToken', {}).get('symbol')}/{p.get('quoteToken', {}).get('symbol')}"
                    )
                    continue

                if not _has_sufficient_volume(p):
                    logger.debug(
                        f"[token_resolver] Skipping low-volume pair: "
                        f"{p.get('baseToken', {}).get('symbol')}/{p.get('quoteToken', {}).get('symbol')} "
                        f"(vol=${(p.get('volume') or {}).get('h24', 0):,.0f})"
                    )
                    continue

                token, ch = self._extract_token_from_pair(p, prefer_base=True)
                addr = token.get("address")
                if not addr:
                    continue
                token_key = f"{ch}:{addr}"
                preview = self._pair_to_preview(p)
                current = best_by_token.get(token_key)
                ds_links = _extract_links_from_preview(preview)
                if not current or (preview.get("liquidity_usd") or 0) > (
                    current.get("best_pair", {}).get("liquidity_usd") or 0
                ):
                    best_by_token[token_key] = {
                        "name": token.get("name"),
                        "symbol": token.get("symbol"),
                        "chain": ch,
                        "address": addr,
                        "coingecko_id": None,
                        "price_usd": preview.get("price_usd"),
                        "market_cap_usd": None,
                        "top_pairs": [preview],
                        "links": self._merge_links({}, ds_links),
                        "_all_pairs": [p],
                    }
                else:
                    best_by_token[token_key]["_all_pairs"].append(p)
                    best_by_token[token_key]["links"] = self._merge_links(best_by_token[token_key]["links"], ds_links)

            out = []
            for token_key, obj in best_by_token.items():
                previews = sorted(
                    [self._pair_to_preview(p) for p in obj["_all_pairs"]],
                    key=lambda x: (x.get("liquidity_usd") or 0),
                    reverse=True,
                )[:3]
                obj["top_pairs"] = previews
                obj.pop("_all_pairs", None)
                out.append(obj)

            out = sorted(out, key=lambda x: (x.get("top_pairs", [{}])[0].get("liquidity_usd") or 0), reverse=True)[
                :limit
            ]

        # Symbol/Name/CGID path
        else:  # qtype in {"symbol", "name", "coingecko_id"}
            cg_anchor = None
            contract_to_cgid_map = {}

            if qtype in {"symbol", "name", "coingecko_id"}:
                # CoinGecko IDs are lowercase, so convert query for lookup
                cg_query = query.lower() if qtype in {"symbol", "coingecko_id"} else query
                cg = await self._cg_get_token_info(cg_query)
                if cg and cg.get("status") != "error":
                    ti = cg.get("token_info") or {}
                    mm = cg.get("market_metrics") or {}
                    links = ti.get("links") or {}
                    symbol_upper = (ti.get("symbol") or "").upper() if ti.get("symbol") else None
                    cg_anchor = {
                        "name": ti.get("name"),
                        "symbol": symbol_upper,
                        "chain": None,
                        "address": None,
                        "coingecko_id": ti.get("id"),
                        "price_usd": mm.get("current_price_usd"),
                        "market_cap_usd": mm.get("market_cap_usd"),
                        "top_pairs": [],
                        "links": {
                            "website": links.get("website"),
                            "twitter": links.get("twitter"),
                            "telegram": links.get("telegram"),
                            "github": links.get("github"),
                            "explorers": links.get("explorers"),
                        },
                    }

                    # Build contract address mapping
                    platforms = cg.get("platforms", {})
                    cgid = ti.get("id")
                    for platform_id, address in platforms.items():
                        if address and cgid:
                            ds_chain = _normalize_platform_name(platform_id)
                            contract_key = f"{ds_chain}:{address.lower()}"
                            contract_to_cgid_map[contract_key] = cgid
                    logger.info(
                        f"[token_resolver] CoinGecko platforms: {len(platforms)}, contract mappings: {len(contract_to_cgid_map)}"
                    )

            ds = await self._ds_search_pairs(query)
            pairs = ((ds or {}).get("data") or {}).get("pairs") or ds.get("pairs") or []
            logger.info(f"[token_resolver] DexScreener returned {len(pairs)} pairs")
            token_map: Dict[str, Dict[str, Any]] = {}

            for p in pairs:
                # Skip invalid same-symbol pairs
                if _is_same_symbol_pair(p):
                    logger.debug(
                        f"[token_resolver] Skipping invalid same-symbol pair: "
                        f"{p.get('baseToken', {}).get('symbol')}/{p.get('quoteToken', {}).get('symbol')}"
                    )
                    continue

                # Skip pairs with insufficient volume
                if not _has_sufficient_volume(p):
                    logger.debug(
                        f"[token_resolver] Skipping low-volume pair: "
                        f"{p.get('baseToken', {}).get('symbol')}/{p.get('quoteToken', {}).get('symbol')} "
                        f"(vol=${(p.get('volume') or {}).get('h24', 0):,.0f})"
                    )
                    continue

                base = p.get("baseToken") or {}
                quote = p.get("quoteToken") or {}
                base_symbol = base.get("symbol", "").upper()
                quote_symbol = quote.get("symbol", "").upper()
                selected = []

                if qtype == "symbol":
                    # Trust DexScreener's search - if it returned this pair for the query, both tokens are potentially relevant
                    # Prefer exact symbol matches but include all to let liquidity ranking decide
                    if base_symbol == query.upper():
                        selected.append(base)
                    if quote_symbol == query.upper():
                        selected.append(quote)
                    # If no exact matches, include both tokens (DexScreener found them for a reason)
                    if not selected:
                        selected.extend([base, quote])
                elif qtype == "name":
                    # Similar approach for name queries
                    if base.get("name", "").lower() == query.lower():
                        selected.append(base)
                    if quote.get("name", "").lower() == query.lower():
                        selected.append(quote)
                    if not selected:
                        selected.extend([base, quote])
                elif qtype == "coingecko_id":
                    # DS doesn't expose CG id; we still keep all to let liquidity sort do the work
                    selected.extend([base, quote])

                # Extract pair-level links once
                preview = self._pair_to_preview(p)

                for tok in selected:
                    addr = tok.get("address")
                    ch = p.get("chainId")
                    if not addr or not ch:
                        continue
                    token_key = f"{ch}:{addr.lower()}"

                    # Only assign pair metadata (websites/socials) if this token matches the query
                    # AND is the base token (DexScreener puts base token metadata in pair info)
                    should_get_links = False
                    if qtype == "symbol":
                        should_get_links = (
                            tok.get("symbol", "").upper() == query.upper()
                            and tok == base  # Only if this is the base token
                        )
                    elif qtype == "name":
                        should_get_links = (
                            tok.get("name", "").lower() == query.lower()
                            and tok == base  # Only if this is the base token
                        )
                    elif qtype == "coingecko_id":
                        # For CG queries, only use base token metadata
                        should_get_links = tok == base

                    ds_links = _extract_links_from_preview(preview) if should_get_links else {}
                    current = token_map.get(token_key)
                    if not current:
                        # First time seeing this token
                        token_map[token_key] = {
                            "name": tok.get("name"),
                            "symbol": tok.get("symbol"),
                            "chain": ch,
                            "address": addr.lower(),
                            "coingecko_id": None,
                            "price_usd": preview.get("price_usd"),
                            "market_cap_usd": None,
                            "top_pairs": [preview],
                            "links": self._merge_links({}, ds_links),
                            "_all_pairs": [p],
                            "_max_liq": preview.get("liquidity_usd") or 0,
                        }
                    else:
                        # Add this pair to the token's collection
                        token_map[token_key]["_all_pairs"].append(p)
                        token_map[token_key]["links"] = self._merge_links(token_map[token_key]["links"], ds_links)

                        # Update metadata if this pair has higher liquidity
                        pair_liq = preview.get("liquidity_usd") or 0
                        if pair_liq > token_map[token_key]["_max_liq"]:
                            token_map[token_key]["_max_liq"] = pair_liq
                            token_map[token_key]["price_usd"] = preview.get("price_usd")

            ds_candidates = []
            linked_count = 0
            for token_key, obj in token_map.items():
                # Try to link with CoinGecko ID
                if contract_to_cgid_map and not obj.get("coingecko_id"):
                    obj_chain = obj.get("chain")
                    address = obj.get("address")
                    if obj_chain and address:
                        contract_key = f"{obj_chain}:{address.lower()}"
                        if contract_key in contract_to_cgid_map:
                            obj["coingecko_id"] = contract_to_cgid_map[contract_key]
                            linked_count += 1

                previews = sorted(
                    [self._pair_to_preview(p) for p in obj["_all_pairs"]],
                    key=lambda x: (x.get("liquidity_usd") or 0),
                    reverse=True,
                )[:3]
                obj["top_pairs"] = previews
                obj.pop("_all_pairs", None)
                obj.pop("_max_liq", None)  # Clean up internal tracking field
                ds_candidates.append(obj)

            ds_candidates = sorted(
                ds_candidates, key=lambda x: (x.get("top_pairs", [{}])[0].get("liquidity_usd") or 0), reverse=True
            )
            logger.info(
                f"[token_resolver] Token map processed: {len(token_map)} unique tokens, {len(ds_candidates)} final candidates, {linked_count} linked to CoinGecko"
            )

            # Merge CoinGecko anchor with DEX candidates that share the same coingecko_id
            combined: List[Dict[str, Any]] = []
            cg_merged = False

            if cg_anchor and cg_anchor.get("coingecko_id"):
                # Try to find a DEX candidate with matching coingecko_id
                cgid = cg_anchor["coingecko_id"]
                for ds_cand in ds_candidates:
                    if ds_cand.get("coingecko_id") == cgid:
                        # Merge CoinGecko market data into DEX candidate
                        ds_cand["market_cap_usd"] = cg_anchor.get("market_cap_usd")
                        # Use CoinGecko price if DEX price is missing or significantly different
                        if not ds_cand.get("price_usd"):
                            ds_cand["price_usd"] = cg_anchor.get("price_usd")
                        cg_merged = True
                        logger.info(f"[token_resolver] Merged CoinGecko data into DEX result for {cgid}")
                        break

                # Only add CoinGecko anchor separately if it wasn't merged
                if not cg_merged:
                    combined.append(cg_anchor)

            combined.extend(ds_candidates)
            out = combined
            logger.info(
                f"[token_resolver] Combined results: CG anchor={1 if (cg_anchor and not cg_merged) else 0}, DS candidates={len(ds_candidates)}, merged={1 if cg_merged else 0}, total={len(out)}"
            )

            if chain:
                filtered = []
                for item in combined:
                    if item.get("chain") is None and item.get("symbol"):
                        # Native token matches any chain filter
                        filtered.append(item)
                    elif item.get("chain") == chain:
                        filtered.append(item)
                out = filtered

        final_results = out[:limit]

        enriched_results = []
        for result in final_results:
            if result.get("coingecko_id"):
                enriched = await self._enrich_with_profile_data(result)
                enriched_results.append(enriched)
            else:
                enriched_results.append(result)

        # Clean empty fields from results
        cleaned_results = [_clean_empty_fields(result) for result in enriched_results]

        logger.info(f"[token_resolver] Final results: {len(final_results)}/{len(out)} (limit={limit})")

        return {"status": "success", "data": {"results": cleaned_results, "timestamp": datetime.utcnow().isoformat()}}

    @with_retry(max_retries=2)
    async def _profile(
        self,
        chain: Optional[str],
        address: Optional[str],
        symbol: Optional[str],
        coingecko_id: Optional[str],
        include: List[str],
        top_n_pairs: int,
        indicator_interval: str,
    ) -> Dict[str, Any]:
        chain = _normalize_chain(chain)

        # Determine token type based on parameters
        is_native = bool(symbol and not (chain and address))
        is_contract = bool(chain and address)

        prof: Dict[str, Any] = {
            "name": None,
            "symbol": symbol.upper() if symbol else None,
            "contracts": {},
            "coingecko_id": coingecko_id,
            "categories": [],
            "links": {},
            "fundamentals": None,
            "supply": None,
            "price_extremes": None,
            "best_pool": None,
            "top_pools": [],
            "extras": {},
            "timestamp": datetime.utcnow().isoformat(),
        }

        # Add contract info if this is a contract token
        if is_contract:
            prof["contracts"][chain] = address

        # Always get CoinGecko data when available
        cg_query = coingecko_id
        if not cg_query and symbol:
            cg_query = symbol.lower()

        if cg_query:
            cg = await self._cg_get_token_info(cg_query)
            if cg and not cg.get("error"):
                ti = cg.get("token_info") or {}
                mm = cg.get("market_metrics") or {}
                prof["name"] = prof["name"] or ti.get("name")
                if ti.get("symbol"):
                    prof["symbol"] = (ti.get("symbol") or "").upper()
                if not prof.get("coingecko_id"):
                    prof["coingecko_id"] = ti.get("id")
                prof["categories"] = ti.get("categories") or prof["categories"]
                links = ti.get("links") or {}
                prof["links"] = self._merge_links(prof["links"], links)
                prof["fundamentals"] = {
                    "price_usd": mm.get("current_price_usd"),
                    "market_cap_usd": mm.get("market_cap_usd"),
                    "fdv_usd": (cg.get("market_metrics") or {}).get("fully_diluted_valuation_usd"),
                    "volume_all_cex_dex_24h_usd": mm.get("total_volume_usd"),
                }
                cex_data = cg.get("cex_data")
                if cex_data:
                    prof["cex_data"] = cex_data
                if cg.get("supply_info") or cg.get("price_metrics"):
                    si = cg.get("supply_info") or {}
                    pm = cg.get("price_metrics") or {}
                    prof["supply"] = {
                        "circulating": si.get("circulating_supply"),
                        "total": si.get("total_supply"),
                        "max": si.get("max_supply"),
                    }
                    prof["price_extremes"] = {
                        "ath_usd": pm.get("ath_usd"),
                        "ath_date": pm.get("ath_date"),
                        "atl_usd": pm.get("atl_usd"),
                        "atl_date": pm.get("atl_date"),
                    }

        # Pairs (DexScreener) and collect websites/socials
        if "pairs" in include or (not include):
            pairs_out = []
            if is_native and prof.get("symbol"):
                ds = await self._ds_search_pairs(prof["symbol"])
                pairs = ((ds or {}).get("data") or {}).get("pairs") or ds.get("pairs") or []
                cand_previews = []
                for p in pairs:
                    # Skip invalid same-symbol pairs
                    if _is_same_symbol_pair(p):
                        continue

                    # Skip pairs with insufficient volume
                    if not _has_sufficient_volume(p):
                        continue

                    base = p.get("baseToken") or {}
                    quote = p.get("quoteToken") or {}
                    base_symbol = base.get("symbol", "").upper()
                    quote_symbol = quote.get("symbol", "").upper()

                    if base_symbol == prof["symbol"] or quote_symbol == prof["symbol"]:
                        prev = self._pair_to_preview(p)
                        cand_previews.append(prev)
                        # merge pair websites/socials into links
                        ds_links = _extract_links_from_preview(prev)
                        prof["links"] = self._merge_links(prof["links"], ds_links)
                pairs_out = sorted(cand_previews, key=lambda x: (x.get("liquidity_usd") or 0), reverse=True)[
                    :top_n_pairs
                ]
            elif is_contract and chain and address:
                ds = await self._ds_token_pairs(chain or "all", address)
                ps = ((ds or {}).get("data") or {}).get("pairs") or []

                # Filter out invalid same-symbol pairs and low-volume pairs
                valid_pairs = [p for p in ps if not _is_same_symbol_pair(p) and _has_sufficient_volume(p)]

                pairs_out = sorted(
                    [self._pair_to_preview(p) for p in valid_pairs],
                    key=lambda x: (x.get("liquidity_usd") or 0),
                    reverse=True,
                )[:top_n_pairs]
                if valid_pairs:
                    base = valid_pairs[0].get("baseToken") or {}
                    prof["name"] = prof["name"] or base.get("name")
                    prof["symbol"] = prof["symbol"] or (base.get("symbol") or "").upper()
                # merge links from pairs
                for prev in pairs_out:
                    ds_links = _extract_links_from_preview(prev)
                    prof["links"] = self._merge_links(prof["links"], ds_links)

            if pairs_out:
                prof["top_pools"] = pairs_out
                prof["best_pool"] = pairs_out[0]

        # Optional: GMGN (if contract + chain supported by gmgn)
        if is_contract and chain and address:
            if chain in {"eth", "ethereum", "base", "bsc", "solana"}:
                ch_map = {"ethereum": "eth", "eth": "eth", "base": "base", "bsc": "bsc", "solana": "sol"}
                gmgn = await self._gmgn_token_info(ch_map.get(chain, chain), address)
                if gmgn and not gmgn.get("error") and gmgn.get("status") != "no_data":
                    # Try to parse payload string quickly for website/twitter/telegram
                    payload = gmgn.get("data", {}).get("payload") if isinstance(gmgn, dict) else None
                    links = {}
                    if isinstance(payload, str):
                        # very light extraction
                        m_web = re.findall(r"Website:\s*(\S+)", payload)
                        m_tw = re.findall(r"Twitter:\s*([^\s]+)", payload)
                        m_tg = re.findall(r"Telegram:\s*(\S+)", payload)
                        links = {
                            "website": m_web or [],
                            "twitter": [f"https://twitter.com/{x}" if not x.startswith("http") else x for x in m_tw],
                            "telegram": m_tg or [],
                        }
                    prof["links"] = self._merge_links(prof["links"], links)
                    prof["extras"]["gmgn"] = {"raw": payload} if payload else gmgn

        # Optional: Solana holders/traders
        if "holders" in include or "traders" in include:
            if chain == "solana" and address:
                if "holders" in include:
                    holders = await self._bq_solana_holders(address, limit=5)
                    if holders and not holders.get("error"):
                        prof["extras"]["holders"] = holders
                if "traders" in include:
                    traders = await self._bq_solana_traders(address, limit=5)
                    if traders and not traders.get("error"):
                        prof["extras"]["traders"] = traders

        # Optional: Funding rates + Technical indicators for large caps
        sym = (symbol or prof.get("symbol") or "").upper()
        if "funding_rates" in include:
            fr = await self._funding_rates(sym)
            if fr and not fr.get("error"):
                prof["extras"]["funding_rates"] = fr

        if "technical_indicators" in include and sym:
            yf_symbol = f"{sym}-USD"
            ind = await self._yahoo_indicator_snapshot(
                yf_symbol, interval=indicator_interval or YF_DEFAULT_INTERVAL, period=YF_DEFAULT_PERIOD
            )
            if ind and not ind.get("error") and ind.get("status") != "no_data":
                prof["extras"]["technical_indicators"] = ind

        return {"status": "success", "data": prof}

    # -----------------------------
    # Tool handler
    # -----------------------------
    async def _handle_tool_logic(
        self, tool_name: str, function_args: dict, session_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        logger.info(f"[token_resolver] Tool call: {tool_name} args={function_args}")

        try:
            if tool_name == "search":
                query = function_args.get("query", "")
                chain = function_args.get("chain")
                type_hint = function_args.get("type_hint")
                limit = 5
                qtype = self._detect_query_type(query, type_hint)
                result = await self._search(query=query, chain=chain, qtype=qtype, limit=limit)
                if errors := self._handle_error(result):
                    return errors
                return result

            elif tool_name == "profile":
                chain = function_args.get("chain")
                address = function_args.get("address")
                symbol = function_args.get("symbol")
                coingecko_id = function_args.get("coingecko_id")
                include = function_args.get("include") or ["pairs"]
                top_n_pairs = int(function_args.get("top_n_pairs", 3))
                indicator_interval = function_args.get("indicator_interval", "1d")

                result = await self._profile(
                    chain=chain,
                    address=address,
                    symbol=symbol,
                    coingecko_id=coingecko_id,
                    include=include,
                    top_n_pairs=top_n_pairs,
                    indicator_interval=indicator_interval,
                )
                if errors := self._handle_error(result):
                    return errors
                return result

            else:
                return {"status": "error", "error": f"Unsupported tool: {tool_name}"}

        except Exception as e:
            logger.exception(f"[token_resolver] Tool execution failed: {e}")
            return {"status": "error", "error": f"Unhandled exception: {e}"}
