import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.token_resolver_agent import TokenResolverAgent
from mesh.tests._test_agents import test_agent

TEST_CASES = {
    # ==================== SEARCH TESTS ====================
    # Large caps
    "search_btc_symbol": {
        "input": {"tool": "search", "tool_arguments": {"query": "BTC"}, "raw_data_only": True},
        "description": "Search for Bitcoin by symbol",
    },
    "search_eth_symbol": {
        "input": {"tool": "search", "tool_arguments": {"query": "ETH"}, "raw_data_only": True},
        "description": "Search for Ethereum by symbol",
    },
    "search_bitcoin_name": {
        "input": {"tool": "search", "tool_arguments": {"query": "Bitcoin", "type_hint": "name"}, "raw_data_only": True},
        "description": "Search for Bitcoin by exact name",
    },
    "search_ethereum_cgid": {
        "input": {
            "tool": "search",
            "tool_arguments": {"query": "ethereum", "type_hint": "coingecko_id"},
            "raw_data_only": True,
        },
        "description": "Search for Ethereum by CoinGecko ID",
    },
    # Medium/Small caps
    "search_link_symbol": {
        "input": {"tool": "search", "tool_arguments": {"query": "LINK"}, "raw_data_only": True},
        "description": "Search for Chainlink by symbol",
    },
    "search_arbitrum_name": {
        "input": {
            "tool": "search",
            "tool_arguments": {"query": "Arbitrum", "type_hint": "name"},
            "raw_data_only": True,
        },
        "description": "Search for Arbitrum by name",
    },
    # Memecoins
    "search_pepe_symbol": {
        "input": {"tool": "search", "tool_arguments": {"query": "PEPE"}, "raw_data_only": True},
        "description": "Search for PEPE memecoin by symbol",
    },
    "search_shib_symbol": {
        "input": {"tool": "search", "tool_arguments": {"query": "SHIB"}, "raw_data_only": True},
        "description": "Search for Shiba Inu by symbol",
    },
    "search_bonk_symbol": {
        "input": {"tool": "search", "tool_arguments": {"query": "BONK"}, "raw_data_only": True},
        "description": "Search for BONK on Solana",
    },
    # Contract addresses - INCLUDING YOUR SPECIFIC TESTS
    "search_heu_base_address": {
        "input": {
            "tool": "search",
            "tool_arguments": {"query": "0xEF22cb48B8483dF6152e1423b19dF5553BbD818b", "chain": "base"},
            "raw_data_only": True,
        },
        "description": "Search for Heurist token on Base by address",
    },
    "search_usdc_solana_address": {
        "input": {
            "tool": "search",
            "tool_arguments": {"query": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v", "chain": "solana"},
            "raw_data_only": True,
        },
        "description": "Search for USDC on Solana by address",
    },
    "search_wrapped_sol": {
        "input": {
            "tool": "search",
            "tool_arguments": {"query": "So11111111111111111111111111111111111111112"},
            "raw_data_only": True,
        },
        "description": "Search for Wrapped SOL by Solana address",
    },
    # Recent Pumpfun tokens
    "search_recent_pumpfun_1": {
        "input": {
            "tool": "search",
            "tool_arguments": {"query": "98mb39tPFKQJ4Bif8iVg9mYb9wsfPZgpgN1sxoVTpump"},
            "raw_data_only": True,
        },
        "description": "Search for recent Pumpfun token by address",
    },
    # Search without funding rates (default behavior)
    "search_heurist_symbol": {
        "input": {"tool": "search", "tool_arguments": {"query": "heurist", "type_hint": "name"}, "raw_data_only": True},
        "description": "Search for Heurist token - should NOT include funding_rates by default",
    },
    # Chain-specific searches
    "search_arb_on_arbitrum": {
        "input": {
            "tool": "search",
            "tool_arguments": {"query": "ARB", "chain": "arbitrum"},
            "raw_data_only": True,
        },
        "description": "Search for ARB specifically on Arbitrum chain",
    },
    "search_bnb_on_bsc": {
        "input": {
            "tool": "search",
            "tool_arguments": {"query": "BNB", "chain": "bsc"},
            "raw_data_only": True,
        },
        "description": "Search for BNB on BSC chain",
    },
    # ==================== PROFILE TESTS ====================
    # Large caps with different includes
    "profile_btc_fundamentals": {
        "input": {
            "tool": "profile",
            "tool_arguments": {"symbol": "BTC", "include": ["fundamentals"]},
            "raw_data_only": True,
        },
        "description": "BTC profile with fundamentals only",
    },
    "profile_eth_with_pairs": {
        "input": {
            "tool": "profile",
            "tool_arguments": {"symbol": "ETH", "include": ["fundamentals", "pairs"]},
            "raw_data_only": True,
        },
        "description": "ETH profile with fundamentals and pairs",
    },
    "profile_btc_with_funding": {
        "input": {
            "tool": "profile",
            "tool_arguments": {"symbol": "BTC", "include": ["funding_rates"]},
            "raw_data_only": True,
        },
        "description": "BTC profile with funding rates explicitly requested (opt-in, large cap only)",
    },
    "profile_heurist_no_funding": {
        "input": {
            "tool": "profile",
            "tool_arguments": {"coingecko_id": "heurist", "include": ["technical_indicators"]},
            "raw_data_only": True,
        },
        "description": "Heurist profile WITHOUT funding rates (not available on Binance, should not error)",
    },
    "profile_eth_with_indicators": {
        "input": {
            "tool": "profile",
            "tool_arguments": {
                "symbol": "ETH",
                "include": ["fundamentals", "technical_indicators"],
                "indicator_interval": "1d",
            },
            "raw_data_only": True,
        },
        "description": "ETH profile with technical indicators",
    },
    # Canonical ID usage
    "profile_by_canonical_native": {
        "input": {
            "tool": "profile",
            "tool_arguments": {"canonical_token_id": "native:ETH"},
            "raw_data_only": True,
        },
        "description": "Profile using native canonical ID",
    },
    "profile_by_canonical_contract": {
        "input": {
            "tool": "profile",
            "tool_arguments": {
                "canonical_token_id": "base:0xEF22cb48B8483dF6152e1423b19dF5553BbD818b",
                "include": ["fundamentals", "pairs"],
            },
            "raw_data_only": True,
        },
        "description": "Profile using contract canonical ID (HEU on Base)",
    },
    "profile_usdc_solana_canonical": {
        "input": {
            "tool": "profile",
            "tool_arguments": {
                "canonical_token_id": "solana:EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                "include": ["fundamentals", "pairs"],
            },
            "raw_data_only": True,
        },
        "description": "Profile USDC on Solana using canonical ID",
    },
    # Solana-specific features with HOLDERS/TRADERS
    "profile_sol_with_holders": {
        "input": {
            "tool": "profile",
            "tool_arguments": {
                "canonical_token_id": "solana:So11111111111111111111111111111111111111112",
                "include": ["fundamentals", "pairs", "holders"],
            },
            "raw_data_only": True,
        },
        "description": "Wrapped SOL profile with holders (Solana only)",
    },
    "profile_usdc_solana_with_traders": {
        "input": {
            "tool": "profile",
            "tool_arguments": {
                "chain": "solana",
                "address": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                "include": ["fundamentals", "pairs", "traders"],
            },
            "raw_data_only": True,
        },
        "description": "USDC Solana profile with top traders",
    },
    "profile_bonk_with_holders_traders": {
        "input": {
            "tool": "profile",
            "tool_arguments": {
                "symbol": "BONK",
                "chain": "solana",
                "include": ["fundamentals", "pairs", "holders", "traders"],
            },
            "raw_data_only": True,
        },
        "description": "BONK profile with both holders and traders (Solana)",
    },
    # Small/Memecoins
    "profile_pepe_full": {
        "input": {
            "tool": "profile",
            "tool_arguments": {"symbol": "PEPE", "include": ["fundamentals", "pairs"], "top_n_pairs": 5},
            "raw_data_only": True,
        },
        "description": "PEPE memecoin full profile with 5 pairs",
    },
    "profile_shib_by_cgid": {
        "input": {
            "tool": "profile",
            "tool_arguments": {"coingecko_id": "shiba-inu", "include": ["fundamentals", "pairs"]},
            "raw_data_only": True,
        },
        "description": "SHIB profile using CoinGecko ID",
    },
    # ==================== PAIRS TESTS - INCLUDING YOUR SPECIFIC TESTS ====================
    "pairs_btc_default": {
        "input": {"tool": "pairs", "tool_arguments": {"symbol": "BTC"}, "raw_data_only": True},
        "description": "Get BTC trading pairs (default limit 5)",
    },
    "pairs_eth_limit_20": {
        "input": {"tool": "pairs", "tool_arguments": {"symbol": "ETH", "limit": 20}, "raw_data_only": True},
        "description": "Get ETH pairs with max limit",
    },
    "pairs_by_canonical": {
        "input": {
            "tool": "pairs",
            "tool_arguments": {"canonical_token_id": "base:0xEF22cb48B8483dF6152e1423b19dF5553BbD818b", "limit": 10},
            "raw_data_only": True,
        },
        "description": "Get pairs using canonical ID",
    },
    # YOUR SPECIFIC TEST - USDC on Solana pairs
    "pairs_usdc_solana": {
        "input": {
            "tool": "pairs",
            "tool_arguments": {"chain": "solana", "address": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"},
            "raw_data_only": True,
        },
        "description": "Get USDC pairs on Solana by chain+address",
    },
    "pairs_pepe_memecoin": {
        "input": {"tool": "pairs", "tool_arguments": {"symbol": "PEPE", "limit": 10}, "raw_data_only": True},
        "description": "Get PEPE memecoin pairs",
    },
    # ==================== NATURAL LANGUAGE TESTS ====================
    "nl_search_bitcoin": {
        "input": {"query": "Find Bitcoin token"},
        "description": "Natural language search for Bitcoin",
    },
    "nl_profile_eth_full": {
        "input": {"query": "Get full profile for ETH including funding rates and technical indicators"},
        "description": "Natural language ETH profile with extras",
    },
    "nl_pairs_usdc_solana": {
        "input": {"query": "Show me trading pairs for USDC on Solana"},
        "description": "Natural language pairs query for USDC Solana",
    },
    "nl_memecoin_analysis": {
        "input": {"query": "Analyze PEPE memecoin with market data and top pools"},
        "description": "Natural language memecoin analysis",
    },
    # ==================== COMPLEX COMBINATIONS ====================
    "profile_btc_all_extras": {
        "input": {
            "tool": "profile",
            "tool_arguments": {
                "symbol": "BTC",
                "include": ["fundamentals", "pairs", "funding_rates", "technical_indicators"],
                "indicator_interval": "1h",
                "top_n_pairs": 10,
            },
            "raw_data_only": True,
        },
        "description": "BTC with all available extras for large caps",
    },
    "profile_solana_token_full": {
        "input": {
            "tool": "profile",
            "tool_arguments": {
                "chain": "solana",
                "address": "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263",  # Bonk
                "include": ["fundamentals", "pairs", "holders", "traders"],
                "top_n_pairs": 5,
            },
            "raw_data_only": True,
        },
        "description": "Solana token with holders and traders data",
    },
    # Multi-chain tokens
    "search_usdc_multichain": {
        "input": {"tool": "search", "tool_arguments": {"query": "USDC"}, "raw_data_only": True},
        "description": "Search USDC (exists on multiple chains)",
    },
    "profile_usdc_base": {
        "input": {
            "tool": "profile",
            "tool_arguments": {
                "chain": "base",
                "address": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
                "include": ["fundamentals", "pairs"],
            },
            "raw_data_only": True,
        },
        "description": "USDC on Base chain",
    },
    "profile_usdc_ethereum": {
        "input": {
            "tool": "profile",
            "tool_arguments": {
                "chain": "ethereum",
                "address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
                "include": ["fundamentals", "pairs"],
            },
            "raw_data_only": True,
        },
        "description": "USDC on Ethereum",
    },
    # Type hint tests
    "search_with_symbol_hint": {
        "input": {
            "tool": "search",
            "tool_arguments": {"query": "sol", "type_hint": "symbol"},
            "raw_data_only": True,
        },
        "description": "Search with explicit symbol type hint",
    },
    "search_with_address_hint": {
        "input": {
            "tool": "search",
            "tool_arguments": {"query": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v", "type_hint": "address"},
            "raw_data_only": True,
        },
        "description": "Search USDC Solana with explicit address type hint",
    },
    # Large cap variations with all features
    "profile_sol_funding_indicators": {
        "input": {
            "tool": "profile",
            "tool_arguments": {
                "symbol": "SOL",
                "include": ["fundamentals", "funding_rates", "technical_indicators"],
                "indicator_interval": "1h",
            },
            "raw_data_only": True,
        },
        "description": "SOL with funding and 1h indicators",
    },
    "profile_bnb_complete": {
        "input": {
            "tool": "profile",
            "tool_arguments": {
                "symbol": "BNB",
                "include": ["fundamentals", "pairs", "funding_rates", "technical_indicators"],
            },
            "raw_data_only": True,
        },
        "description": "BNB complete profile",
    },
    # Stablecoins
    "search_usdt": {
        "input": {"tool": "search", "tool_arguments": {"query": "USDT"}, "raw_data_only": True},
        "description": "Search for Tether",
    },
    "profile_dai": {
        "input": {
            "tool": "profile",
            "tool_arguments": {"symbol": "DAI", "include": ["fundamentals", "pairs"]},
            "raw_data_only": True,
        },
        "description": "DAI stablecoin profile",
    },
    # L2 tokens
    "search_op_token": {
        "input": {"tool": "search", "tool_arguments": {"query": "OP", "chain": "optimism"}, "raw_data_only": True},
        "description": "Search for Optimism token",
    },
    "profile_matic": {
        "input": {
            "tool": "profile",
            "tool_arguments": {"symbol": "MATIC", "include": ["fundamentals", "pairs"]},
            "raw_data_only": True,
        },
        "description": "Polygon/MATIC profile",
    },
    # DeFi tokens
    "search_uni": {
        "input": {"tool": "search", "tool_arguments": {"query": "UNI"}, "raw_data_only": True},
        "description": "Search for Uniswap token",
    },
    "profile_aave": {
        "input": {
            "tool": "profile",
            "tool_arguments": {"symbol": "AAVE", "include": ["fundamentals", "pairs"], "top_n_pairs": 7},
            "raw_data_only": True,
        },
        "description": "AAVE DeFi token profile",
    },
    # Recent/New tokens
    "search_new_solana_token": {
        "input": {
            "tool": "search",
            "tool_arguments": {"query": "HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC"},
            "raw_data_only": True,
        },
        "description": "Search for newer Solana token",
    },
    "profile_new_memecoin": {
        "input": {
            "tool": "profile",
            "tool_arguments": {
                "chain": "solana",
                "address": "4TBi66vi32S7J8X1A6eWfaLHYmUXu7CStcEmsJQdpump",
                "include": ["fundamentals", "pairs"],
            },
            "raw_data_only": True,
        },
        "description": "Profile of a newer Solana Pumpfun token",
    },
    # Edge cases
    "pairs_no_pools": {
        "input": {
            "tool": "pairs",
            "tool_arguments": {"symbol": "XYZ123"},
            "raw_data_only": True,
        },
        "description": "Pairs for non-existent token (should return empty)",
    },
    "profile_no_identifier": {
        "input": {"tool": "profile", "tool_arguments": {"include": ["fundamentals"]}, "raw_data_only": True},
        "description": "Profile without any identifier (should handle gracefully)",
    },
    # Canonical ID round-trip tests
    "canonical_usdc_solana_workflow": {
        "input": {
            "query": "Search for USDC on Solana (EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v), extract canonical ID, then use it for profile and pairs"
        },
        "description": "Test canonical ID workflow for USDC Solana",
    },
    # Response format tests
    "search_detailed_format": {
        "input": {
            "tool": "search",
            "tool_arguments": {"query": "UNI", "response_format": "detailed"},
            "raw_data_only": True,
        },
        "description": "Search with detailed response format",
    },
    "search_concise_format": {
        "input": {
            "tool": "search",
            "tool_arguments": {"query": "AAVE", "response_format": "concise"},
            "raw_data_only": True,
        },
        "description": "Search with concise response format",
    },
    # Limit variations
    "search_eth_limit_1": {
        "input": {"tool": "search", "tool_arguments": {"query": "ETH", "limit": 1}, "raw_data_only": True},
        "description": "Search ETH with limit 1",
    },
    "pairs_usdc_limit_15": {
        "input": {
            "tool": "pairs",
            "tool_arguments": {
                "chain": "solana",
                "address": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                "limit": 15,
            },
            "raw_data_only": True,
        },
        "description": "USDC Solana pairs with limit 15",
    },
    # Combined Solana tests with all features
    "profile_usdc_solana_complete": {
        "input": {
            "tool": "profile",
            "tool_arguments": {
                "chain": "solana",
                "address": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                "include": ["fundamentals", "pairs", "holders", "traders"],
                "top_n_pairs": 10,
            },
            "raw_data_only": True,
        },
        "description": "Complete USDC Solana profile with all Solana-specific features",
    },
}

if __name__ == "__main__":
    asyncio.run(test_agent(TokenResolverAgent, TEST_CASES, delay_seconds=5))
