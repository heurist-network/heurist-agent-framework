import json
import logging
import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from decorators import with_cache, with_retry
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

LARGE_CAP_SYMBOLS_FOR_FUNDING = {"BTC", "ETH", "SOL", "XRP", "BNB", "DOGE", "ADA", "AVAX", "LINK", "LTC", "BCH"}
YF_DEFAULT_INTERVAL = "1d"
YF_DEFAULT_PERIOD = "6mo"


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


def _make_canonical_id(
    chain: Optional[str] = None, address: Optional[str] = None, native_symbol: Optional[str] = None
) -> Optional[str]:
    if native_symbol:
        return f"native:{native_symbol.upper()}"
    if chain and address:
        return f"{chain.lower()}:{address}"
    return None


def _parse_canonical_id(cid: str) -> Dict[str, str]:
    out = {"kind": "", "chain": "", "address": "", "symbol": ""}
    if not cid or ":" not in cid:
        return out
    lhs, rhs = cid.split(":", 1)
    if lhs.lower() == "native":
        out["kind"] = "native"
        out["symbol"] = rhs.upper()
        return out
    out["kind"] = "contract"
    out["chain"] = _normalize_chain(lhs)
    out["address"] = rhs
    return out


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
                "tags": ["Token Search", "Market Data"],
                "recommended": True,
                "image_url": "https://raw.githubusercontent.com/heurist-network/heurist-agent-framework/refs/heads/main/mesh/images/Heurist.png",
                "examples": [
                    "search query=ETH",
                    "search query=0xEF22cb48B8483dF6152e1423b19dF5553BbD818b chain=base",
                    "profile canonical_token_id=base:0xEF22cb48B8483dF6152e1423b19dF5553BbD818b include=['fundamentals','pairs']",
                    "profile symbol=BTC include=['fundamentals','funding_rates','technical_indicators']",
                    "pairs chain=solana address=EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v limit=5",
                ],
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
                    "description": "Find tokens by address, ticker/symbol, exact name, or CoinGecko ID. Returns up to 5 concise candidates with basic market/trading context. This tool also returns a canonical ID (in the format of native:<SYMBOL> like native:ETH or <chain>:<contract_address> like base:0xEF22cb48B8483dF6152e1423b19dF5553BbD818b → Heurist token on Base or solana:So11111111111111111111111111111111111111112 → Wrapped SOL on Solana.) Agents can pass the canonical ID around between search, profile, and pairs",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "0x… (EVM), Solana mint, ticker/symbol (e.g., ETH), exact name, or CoinGecko ID",
                            },
                            "chain": {
                                "type": "string",
                                "description": "Optional chain hint (e.g., base, ethereum, solana)",
                            },
                            "type_hint": {
                                "type": "string",
                                "enum": ["address", "symbol", "name", "coingecko_id"],
                                "description": "Optional explicit hint",
                            },
                            "limit": {"type": "integer", "default": 5, "minimum": 1, "maximum": 10},
                            "response_format": {
                                "type": "string",
                                "enum": ["concise", "detailed"],
                                "default": "concise",
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
                    "description": "Hydrate a single token into a detailed profile. Identify it by canonical_token_id or by one of: chain+address, symbol, coingecko_id. Optional sections: fundamentals, pairs, holders (Solana), traders (Solana), funding_rates (large caps only), technical_indicators (large caps only).",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "canonical_token_id": {"type": "string"},
                            "chain": {"type": "string"},
                            "address": {"type": "string"},
                            "symbol": {"type": "string", "description": "Ticker symbol like BTC or ETH"},
                            "coingecko_id": {"type": "string"},
                            "include": {
                                "type": "array",
                                "items": {
                                    "type": "string",
                                    "enum": [
                                        "fundamentals",
                                        "pairs",
                                        "holders",
                                        "traders",
                                        "funding_rates",
                                        "technical_indicators",
                                    ],
                                },
                                "default": ["fundamentals", "pairs"],
                            },
                            "top_n_pairs": {"type": "integer", "default": 3, "minimum": 1, "maximum": 10},
                            "indicator_interval": {"type": "string", "enum": ["1h", "1d"], "default": "1d"},
                        },
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "pairs",
                    "description": "Return top DEX pools for a token, ranked by liquidity, with price/volume snippets. Identify the token by canonical_token_id or by chain+address or by coingecko_id+symbol. Sometimes CEX tokens don't have DEX pools, which is normal.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "canonical_token_id": {"type": "string"},
                            "chain": {"type": "string"},
                            "address": {"type": "string"},
                            "coingecko_id": {"type": "string"},
                            "symbol": {"type": "string"},
                            "limit": {"type": "integer", "default": 5, "minimum": 1, "maximum": 20},
                        },
                        "required": [],
                    },
                },
            },
        ]

    # -----------------------------
    # Bridge to other Mesh agents (cached 300s)
    # -----------------------------
    async def _agent_call(self, module: str, cls: str, tool: str, args: Dict[str, Any]) -> Dict[str, Any]:
        from importlib import import_module

        mod = import_module(module)
        agent_cls = getattr(mod, cls)
        inst = agent_cls()
        if self.heurist_api_key:
            inst.set_heurist_api_key(self.heurist_api_key)
        payload = {"tool": tool, "tool_arguments": args, "raw_data_only": True, "session_context": {}}
        result = await inst.call_agent(payload)
        return result.get("data", result)

    # CoinGecko (prefer existing agent; fallback to public API)
    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def _cg_get_token_info(self, query_or_id: str) -> Dict[str, Any]:
        try:
            return await self._agent_call(
                "mesh.agents.coingecko_token_info_agent",
                "CoinGeckoTokenInfoAgent",
                "get_token_info",
                {"coingecko_id": query_or_id},
            )
        except Exception as e:
            logger.warning(f"[token_resolver] CG get_token_info fallback: {e}")
            search_url = "https://api.coingecko.com/api/v3/search"
            s = await self._api_request(search_url, params={"query": query_or_id})
            if "error" in s or "coins" not in s:
                return {"status": "error", "error": f"CoinGecko search failed for {query_or_id}"}
            coins = [c for c in s.get("coins", []) if c.get("id")]
            if not coins:
                return {"status": "no_data", "error": f"No CoinGecko match for {query_or_id}"}
            cgid = coins[0]["id"]
            coin_url = f"https://api.coingecko.com/api/v3/coins/{cgid}"
            c = await self._api_request(coin_url)
            if "error" in c:
                return {"status": "error", "error": f"CoinGecko coin fetch failed for {cgid}"}
            links = c.get("links") or {}
            pages = links.get("homepage") or []
            homepage = next((u for u in pages if u), None)
            twitter = links.get("twitter_screen_name") or None
            telegram = links.get("telegram_channel_identifier") or None
            github = (links.get("repos_url") or {}).get("github", [])
            explorers = c.get("links", {}).get("blockchain_site", []) or []
            categories = c.get("categories", []) or []
            mkt = c.get("market_data") or {}
            return {
                "token_info": {
                    "id": c.get("id"),
                    "name": c.get("name"),
                    "symbol": c.get("symbol"),
                    "categories": categories,
                    "links": {
                        "website": homepage,
                        "twitter": f"https://twitter.com/{twitter}" if twitter else None,
                        "telegram": f"https://t.me/{telegram}" if telegram else None,
                        "github": github,
                        "explorers": [u for u in explorers if u],
                    },
                },
                "market_metrics": {
                    "current_price_usd": (mkt.get("current_price") or {}).get("usd"),
                    "market_cap_usd": (mkt.get("market_cap") or {}).get("usd"),
                    "fully_diluted_valuation_usd": (mkt.get("fully_diluted_valuation") or {}).get("usd"),
                    "total_volume_usd": (mkt.get("total_volume") or {}).get("usd"),
                },
                "supply_info": {
                    "circulating_supply": mkt.get("circulating_supply"),
                    "total_supply": mkt.get("total_supply"),
                    "max_supply": mkt.get("max_supply"),
                },
                "price_metrics": {
                    "ath_usd": (mkt.get("ath") or {}).get("usd"),
                    "ath_date": (mkt.get("ath_date") or {}).get("usd"),
                    "atl_usd": (mkt.get("atl") or {}).get("usd"),
                    "atl_date": (mkt.get("atl_date") or {}).get("usd"),
                },
            }

    # DexScreener
    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def _ds_search_pairs(self, search_term: str) -> Dict[str, Any]:
        try:
            return await self._agent_call(
                "mesh.agents.dexscreener_token_info_agent",
                "DexScreenerTokenInfoAgent",
                "search_pairs",
                {"search_term": search_term},
            )
        except Exception as e:
            logger.warning(f"[token_resolver] DS search_pairs fallback: {e}")
            url = "https://api.dexscreener.com/latest/dex/search"
            return await self._api_request(url, params={"q": search_term})

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=3)
    async def _ds_token_pairs(self, chain: Optional[str], token_address: str) -> Dict[str, Any]:
        try:
            return await self._agent_call(
                "mesh.agents.dexscreener_token_info_agent",
                "DexScreenerTokenInfoAgent",
                "get_token_pairs",
                {"chain": chain or "all", "token_address": token_address},
            )
        except Exception as e:
            logger.warning(f"[token_resolver] DS get_token_pairs fallback: {e}")
            url = f"https://api.dexscreener.com/latest/dex/tokens/{token_address}"
            raw = await self._api_request(url)
            if "error" in raw:
                return raw
            pairs = raw.get("pairs", []) or []
            if chain and chain.lower() != "all":
                pairs = [p for p in pairs if p.get("chainId") == chain.lower()]
            return {"status": "success", "data": {"pairs": pairs}}

    # GMGN / Unifai (memecoins)
    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=2)
    async def _gmgn_token_info(self, chain: str, address: str) -> Dict[str, Any]:
        try:
            return await self._agent_call(
                "mesh.agents.unifai_token_analysis_agent",
                "UnifaiTokenAnalysisAgent",
                "get_gmgn_token_info",
                {"chain": chain, "address": address},
            )
        except Exception as e:
            logger.info(f"[token_resolver] GMGN unavailable: {e}")
            return {"status": "no_data", "error": "gmgn_unavailable"}

    # Bitquery (Solana)
    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=2)
    async def _bq_solana_holders(self, mint: str, limit: int = 5) -> Dict[str, Any]:
        try:
            return await self._agent_call(
                "mesh.agents.bitquery_solana_token_info_agent",
                "BitquerySolanaTokenInfoAgent",
                "query_token_holders",
                {"token_address": mint, "limit": limit},
            )
        except Exception as e:
            logger.info(f"[token_resolver] Bitquery holders unavailable: {e}")
            return {"status": "no_data", "error": "bitquery_unavailable"}

    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=2)
    async def _bq_solana_traders(self, mint: str, limit: int = 5) -> Dict[str, Any]:
        try:
            return await self._agent_call(
                "mesh.agents.bitquery_solana_token_info_agent",
                "BitquerySolanaTokenInfoAgent",
                "query_top_traders",
                {"token_address": mint, "limit": limit},
            )
        except Exception as e:
            logger.info(f"[token_resolver] Bitquery traders unavailable: {e}")
            return {"status": "no_data", "error": "bitquery_unavailable"}

    # Funding rates (Coinsider)
    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=2)
    async def _funding_rates(self, symbol: str) -> Dict[str, Any]:
        try:
            return await self._agent_call(
                "mesh.agents.funding_rate_agent",
                "FundingRateAgent",
                "get_symbol_funding_rates",
                {"symbol": symbol},
            )
        except Exception as e:
            logger.info(f"[token_resolver] Funding rates unavailable: {e}")
            return {"status": "no_data", "error": "funding_unavailable"}

    # Yahoo Finance indicators (optional)
    @with_cache(ttl_seconds=300)
    @with_retry(max_retries=2)
    async def _yahoo_indicator_snapshot(
        self, yf_symbol: str, interval: str = YF_DEFAULT_INTERVAL, period: str = YF_DEFAULT_PERIOD
    ) -> Dict[str, Any]:
        try:
            return await self._agent_call(
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
        if _is_evm_address(q) or _is_solana_address(q):
            return "address"
        if re.fullmatch(r"[A-Za-z0-9\-]{2,20}", q) and q.upper() == q:
            return "symbol"
        if re.fullmatch(r"[a-z0-9\-]{2,64}", q):
            return "coingecko_id"
        letters = re.sub(r"[^A-Za-z]", "", q)
        if len(letters) >= 3 and " " in q:
            return "name"
        return "unknown"

    def _pair_to_preview(self, p: Dict[str, Any]) -> Dict[str, Any]:
        vol = (p.get("volume") or {}).get("h24")
        liq = (p.get("liquidity") or {}).get("usd")
        info = p.get("info") or {}
        return {
            "chain": p.get("chainId"),
            "dex": p.get("dexId"),
            "pair_address": p.get("pairAddress"),
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
            "address": chosen.get("address"),
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
    @with_retry(max_retries=2)
    async def _search(
        self, query: str, chain: Optional[str], qtype: str, limit: int, response_format: str
    ) -> Dict[str, Any]:
        chain = _normalize_chain(chain)
        results: List[Dict[str, Any]] = []

        if qtype == "unknown":
            return {
                "status": "error",
                "error": "Unsupported or vague query. Provide address, symbol, exact name, or CoinGecko ID.",
            }

        if qtype == "address":
            pairs_res = await self._ds_token_pairs(chain or "all", query)
            pairs = ((pairs_res or {}).get("data") or {}).get("pairs") or []
            if not pairs:
                if chain:
                    results.append(
                        {
                            "id": _make_canonical_id(chain=chain, address=query),
                            "name": None,
                            "symbol": None,
                            "chain": chain,
                            "address": query,
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
                token, ch = self._extract_token_from_pair(p, prefer_base=True)
                addr = token.get("address")
                if not addr:
                    continue
                cid = _make_canonical_id(chain=ch, address=addr)
                preview = self._pair_to_preview(p)
                current = best_by_token.get(cid)
                # collect websites/socials
                ds_links = {
                    "website": preview.get("websites"),
                    "twitter": [s.get("url") for s in preview.get("socials", []) if (s or {}).get("type") == "twitter"],
                }
                if not current or (preview.get("liquidity_usd") or 0) > (
                    current.get("best_pair", {}).get("liquidity_usd") or 0
                ):
                    best_by_token[cid] = {
                        "id": cid,
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
                    best_by_token[cid]["_all_pairs"].append(p)
                    best_by_token[cid]["links"] = self._merge_links(best_by_token[cid]["links"], ds_links)

            out = []
            for cid, obj in best_by_token.items():
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
            if qtype in {"symbol", "name", "coingecko_id"}:
                cg = await self._cg_get_token_info(query)
                if cg and not cg.get("error"):
                    ti = cg.get("token_info") or {}
                    mm = cg.get("market_metrics") or {}
                    links = ti.get("links") or {}
                    cg_anchor = {
                        "id": _make_canonical_id(native_symbol=(ti.get("symbol") or "").upper())
                        if ti.get("symbol")
                        else None,
                        "name": ti.get("name"),
                        "symbol": (ti.get("symbol") or "").upper() if ti.get("symbol") else None,
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

            ds = await self._ds_search_pairs(query)
            pairs = ((ds or {}).get("data") or {}).get("pairs") or ds.get("pairs") or []
            token_map: Dict[str, Dict[str, Any]] = {}

            for p in pairs:
                base = p.get("baseToken") or {}
                quote = p.get("quoteToken") or {}
                selected = []

                if qtype == "symbol":
                    if base.get("symbol", "").upper() == query.upper():
                        selected.append(base)
                    if quote.get("symbol", "").upper() == query.upper():
                        selected.append(quote)
                elif qtype == "name":
                    if base.get("name", "").lower() == query.lower():
                        selected.append(base)
                    if quote.get("name", "").lower() == query.lower():
                        selected.append(quote)
                elif qtype == "coingecko_id":
                    # DS doesn't expose CG id; we still keep all to let liquidity sort do the work
                    selected.extend([base, quote])

                for tok in selected:
                    addr = tok.get("address")
                    ch = p.get("chainId")
                    if not addr or not ch:
                        continue
                    cid = _make_canonical_id(chain=ch, address=addr)
                    preview = self._pair_to_preview(p)
                    ds_links = {
                        "website": preview.get("websites"),
                        "twitter": [
                            s.get("url") for s in preview.get("socials", []) if (s or {}).get("type") == "twitter"
                        ],
                        "telegram": [
                            s.get("url") for s in preview.get("socials", []) if (s or {}).get("type") == "telegram"
                        ],
                    }
                    current = token_map.get(cid)
                    if not current or (preview.get("liquidity_usd") or 0) > (
                        current.get("best_pair", {}).get("liquidity_usd") or 0
                    ):
                        token_map[cid] = {
                            "id": cid,
                            "name": tok.get("name"),
                            "symbol": tok.get("symbol"),
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
                        token_map[cid]["_all_pairs"].append(p)
                        token_map[cid]["links"] = self._merge_links(token_map[cid]["links"], ds_links)

            ds_candidates = []
            for cid, obj in token_map.items():
                previews = sorted(
                    [self._pair_to_preview(p) for p in obj["_all_pairs"]],
                    key=lambda x: (x.get("liquidity_usd") or 0),
                    reverse=True,
                )[:3]
                obj["top_pairs"] = previews
                obj.pop("_all_pairs", None)
                ds_candidates.append(obj)

            ds_candidates = sorted(
                ds_candidates, key=lambda x: (x.get("top_pairs", [{}])[0].get("liquidity_usd") or 0), reverse=True
            )

            combined: List[Dict[str, Any]] = []
            if cg_anchor:
                combined.append(cg_anchor)
            combined.extend(ds_candidates)
            out = combined

            if chain:
                filtered = []
                for item in combined:
                    if item.get("chain") is None and item.get("id", "").startswith("native:"):
                        filtered.append(item)
                    elif item.get("chain") == chain:
                        filtered.append(item)
                out = filtered

        final_results = out[:limit]

        if response_format == "concise":
            concise_results = []
            for item in final_results:
                concise_item = {
                    "id": item.get("id"),
                    "name": item.get("name"),
                    "symbol": item.get("symbol"),
                    "chain": item.get("chain"),
                    "address": item.get("address"),
                    "price_usd": item.get("price_usd"),
                    "market_cap_usd": item.get("market_cap_usd"),
                }
                if item.get("top_pairs"):
                    best_pair = item["top_pairs"][0]
                    concise_item["best_pool"] = {
                        "dex": best_pair.get("dex"),
                        "price_usd": best_pair.get("price_usd"),
                        "liquidity_usd": best_pair.get("liquidity_usd"),
                    }
                concise_results.append(concise_item)
            final_results = concise_results

        return {"status": "success", "data": {"results": final_results, "timestamp": datetime.utcnow().isoformat()}}

    @with_retry(max_retries=2)
    async def _profile(
        self,
        canonical_token_id: Optional[str],
        chain: Optional[str],
        address: Optional[str],
        symbol: Optional[str],
        coingecko_id: Optional[str],
        include: List[str],
        top_n_pairs: int,
        indicator_interval: str,
    ) -> Dict[str, Any]:
        cid = canonical_token_id
        chain = _normalize_chain(chain)

        if not cid:
            if chain and address:
                cid = _make_canonical_id(chain=chain, address=address)
            elif symbol:
                cid = _make_canonical_id(native_symbol=symbol.upper())
            elif coingecko_id:
                cg_tmp = await self._cg_get_token_info(coingecko_id)
                ti_tmp = (cg_tmp or {}).get("token_info") or {}
                if ti_tmp.get("symbol"):
                    cid = _make_canonical_id(native_symbol=ti_tmp["symbol"].upper())

        prof: Dict[str, Any] = {
            "id": cid,
            "name": None,
            "symbol": None,
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

        # Fundamentals & links (CoinGecko)
        if "fundamentals" in include or (not include):
            cg_query = coingecko_id
            if not cg_query and symbol:
                cg_query = symbol.lower()
            if not cg_query and cid and cid.startswith("native:"):
                cg_query = cid.split(":", 1)[1].lower()

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
                        "volume24h_usd": mm.get("total_volume_usd"),
                    }
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
            if cid and cid.startswith("native:") and prof.get("symbol"):
                ds = await self._ds_search_pairs(prof["symbol"])
                pairs = ((ds or {}).get("data") or {}).get("pairs") or ds.get("pairs") or []
                cand_previews = []
                for p in pairs:
                    base = p.get("baseToken") or {}
                    quote = p.get("quoteToken") or {}
                    if (
                        base.get("symbol", "").upper() == prof["symbol"]
                        or quote.get("symbol", "").upper() == prof["symbol"]
                    ):
                        prev = self._pair_to_preview(p)
                        cand_previews.append(prev)
                        # merge pair websites/socials into links
                        ds_links = {
                            "website": prev.get("websites"),
                            "twitter": [
                                s.get("url") for s in prev.get("socials", []) if (s or {}).get("type") == "twitter"
                            ],
                            "telegram": [
                                s.get("url") for s in prev.get("socials", []) if (s or {}).get("type") == "telegram"
                            ],
                        }
                        prof["links"] = self._merge_links(prof["links"], ds_links)
                pairs_out = sorted(cand_previews, key=lambda x: (x.get("liquidity_usd") or 0), reverse=True)[
                    :top_n_pairs
                ]
            elif cid and ":" in cid:
                parsed = _parse_canonical_id(cid)
                if parsed["kind"] == "contract" and parsed["address"]:
                    ds = await self._ds_token_pairs(parsed["chain"] or chain or "all", parsed["address"])
                    ps = ((ds or {}).get("data") or {}).get("pairs") or []
                    pairs_out = sorted(
                        [self._pair_to_preview(p) for p in ps],
                        key=lambda x: (x.get("liquidity_usd") or 0),
                        reverse=True,
                    )[:top_n_pairs]
                    if ps:
                        base = ps[0].get("baseToken") or {}
                        prof["name"] = prof["name"] or base.get("name")
                        prof["symbol"] = prof["symbol"] or (base.get("symbol") or "").upper()
                        prof["contracts"][parsed["chain"]] = parsed["address"]
                    # merge links from pairs
                    for prev in pairs_out:
                        ds_links = {
                            "website": prev.get("websites"),
                            "twitter": [
                                s.get("url") for s in prev.get("socials", []) if (s or {}).get("type") == "twitter"
                            ],
                            "telegram": [
                                s.get("url") for s in prev.get("socials", []) if (s or {}).get("type") == "telegram"
                            ],
                        }
                        prof["links"] = self._merge_links(prof["links"], ds_links)

            if pairs_out:
                prof["top_pools"] = pairs_out
                prof["best_pool"] = pairs_out[0]

        # Optional: GMGN (if contract + chain supported by gmgn)
        if cid and ":" in cid:
            parsed = _parse_canonical_id(cid)
            ch = parsed["chain"]
            if ch in {"eth", "ethereum", "base", "bsc", "sol"}:
                ch_map = {"ethereum": "eth", "eth": "eth", "base": "base", "bsc": "bsc", "solana": "sol"}
                gmgn = await self._gmgn_token_info(ch_map.get(ch, ch), parsed["address"])
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
            sol_addr = None
            if cid and ":" in cid and cid.split(":")[0] == "solana":
                sol_addr = cid.split(":")[1]
            elif chain == "solana" and address:
                sol_addr = address
            if sol_addr:
                if "holders" in include:
                    holders = await self._bq_solana_holders(sol_addr, limit=5)
                    if holders and not holders.get("error"):
                        prof["extras"]["holders"] = holders
                if "traders" in include:
                    traders = await self._bq_solana_traders(sol_addr, limit=5)
                    if traders and not traders.get("error"):
                        prof["extras"]["traders"] = traders

        # Optional: Funding rates + Technical indicators for large caps
        sym = (symbol or prof.get("symbol") or "").upper()
        if "funding_rates" in include and sym in LARGE_CAP_SYMBOLS_FOR_FUNDING:
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

    @with_retry(max_retries=2)
    async def _pairs(
        self,
        canonical_token_id: Optional[str],
        chain: Optional[str],
        address: Optional[str],
        coingecko_id: Optional[str],
        symbol: Optional[str],
        limit: int,
    ) -> Dict[str, Any]:
        chain = _normalize_chain(chain)
        out: List[Dict[str, Any]] = []

        cid = canonical_token_id
        if not cid:
            if chain and address:
                cid = _make_canonical_id(chain=chain, address=address)
            elif coingecko_id or symbol:
                sym = (symbol or "").upper()
                if not sym and coingecko_id:
                    cg = await self._cg_get_token_info(coingecko_id)
                    ti = (cg or {}).get("token_info") or {}
                    sym = (ti.get("symbol") or "").upper()
                if sym:
                    ds = await self._ds_search_pairs(sym)
                    pairs = ((ds or {}).get("data") or {}).get("pairs") or ds.get("pairs") or []
                    previews = []
                    for p in pairs:
                        base = p.get("baseToken") or {}
                        quote = p.get("quoteToken") or {}
                        if base.get("symbol", "").upper() == sym or quote.get("symbol", "").upper() == sym:
                            previews.append(self._pair_to_preview(p))
                    out = sorted(previews, key=lambda x: (x.get("liquidity_usd") or 0), reverse=True)[:limit]
                    return {"status": "success", "data": {"pairs": out}}
                else:
                    return {"status": "success", "data": {"pairs": []}}

        if cid and ":" in cid:
            parsed = _parse_canonical_id(cid)
            if parsed["kind"] == "contract":
                ds = await self._ds_token_pairs(parsed["chain"] or chain or "all", parsed["address"])
                ps = ((ds or {}).get("data") or {}).get("pairs") or []
                out = sorted(
                    [self._pair_to_preview(p) for p in ps], key=lambda x: (x.get("liquidity_usd") or 0), reverse=True
                )[:limit]

        return {"status": "success", "data": {"pairs": out}}

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
                limit = int(function_args.get("limit", 5))
                response_format = function_args.get("response_format", "concise")

                qtype = self._detect_query_type(query, type_hint)
                result = await self._search(
                    query=query, chain=chain, qtype=qtype, limit=limit, response_format=response_format
                )
                if errors := self._handle_error(result):
                    return errors
                return result

            elif tool_name == "profile":
                cid = function_args.get("canonical_token_id")
                chain = function_args.get("chain")
                address = function_args.get("address")
                symbol = function_args.get("symbol")
                coingecko_id = function_args.get("coingecko_id")
                include = function_args.get("include") or ["fundamentals", "pairs"]
                top_n_pairs = int(function_args.get("top_n_pairs", 3))
                indicator_interval = function_args.get("indicator_interval", "1d")

                result = await self._profile(
                    canonical_token_id=cid,
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

            elif tool_name == "pairs":
                cid = function_args.get("canonical_token_id")
                chain = function_args.get("chain")
                address = function_args.get("address")
                coingecko_id = function_args.get("coingecko_id")
                symbol = function_args.get("symbol")
                limit = int(function_args.get("limit", 5))

                result = await self._pairs(
                    canonical_token_id=cid,
                    chain=chain,
                    address=address,
                    coingecko_id=coingecko_id,
                    symbol=symbol,
                    limit=limit,
                )
                if errors := self._handle_error(result):
                    return errors
                return result

            else:
                return {"status": "error", "error": f"Unsupported tool: {tool_name}"}

        except Exception as e:
            logger.exception(f"[token_resolver] Tool execution failed: {e}")
            return {"status": "error", "error": f"Unhandled exception: {e}"}
