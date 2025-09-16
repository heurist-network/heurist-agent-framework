import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.bitquery_solana_token_info_agent import BitquerySolanaTokenInfoAgent
from mesh.tests._test_agents import test_agent

TEST_CASES = {
    # Test with a query that mentions a token mint address for trading info
    "token_info_by_address": {
        "input": {"query": "Get token info for HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC"},
        "description": "Query that mentions a token mint address for trading info",
    },
    # Test token metrics with different quote tokens - USDC
    "metrics_usdc_natural": {
        "input": {
            "query": "Get market cap and trade volume for 98mb39tPFKQJ4Bif8iVg9mYb9wsfPZgpgN1sxoVTpump using usdc pair"
        },
        "description": "Natural language query for metrics with USDC quote token",
    },
    "metrics_usdc_direct": {
        "input": {
            "tool": "query_token_metrics",
            "tool_arguments": {"token_address": "98mb39tPFKQJ4Bif8iVg9mYb9wsfPZgpgN1sxoVTpump", "quote_token": "usdc"},
            "raw_data_only": True,
        },
        "description": "Direct tool call for metrics with USDC quote token",
    },
    # Test token metrics with SOL quote token
    "metrics_sol_natural": {
        "input": {
            "query": "Get market cap and trade volume for 98mb39tPFKQJ4Bif8iVg9mYb9wsfPZgpgN1sxoVTpump using sol pair"
        },
        "description": "Natural language query for metrics with SOL quote token",
    },
    "metrics_sol_direct": {
        "input": {
            "tool": "query_token_metrics",
            "tool_arguments": {"token_address": "98mb39tPFKQJ4Bif8iVg9mYb9wsfPZgpgN1sxoVTpump", "quote_token": "sol"},
            "raw_data_only": True,
        },
        "description": "Direct tool call for metrics with SOL quote token",
    },
    # Test token metrics with VIRTUAL quote token
    "metrics_virtual_natural": {
        "input": {
            "query": "Get market cap and trade volume for 98mb39tPFKQJ4Bif8iVg9mYb9wsfPZgpgN1sxoVTpump using virtual pair"
        },
        "description": "Natural language query for metrics with VIRTUAL quote token",
    },
    "metrics_virtual_direct": {
        "input": {
            "tool": "query_token_metrics",
            "tool_arguments": {
                "token_address": "98mb39tPFKQJ4Bif8iVg9mYb9wsfPZgpgN1sxoVTpump",
                "quote_token": "virtual",
            },
            "raw_data_only": True,
        },
        "description": "Direct tool call for metrics with VIRTUAL quote token",
    },
    # Test token metrics with native_sol quote token
    "metrics_native_sol_natural": {
        "input": {
            "query": "Get market cap and trade volume for 98mb39tPFKQJ4Bif8iVg9mYb9wsfPZgpgN1sxoVTpump using native_sol pair"
        },
        "description": "Natural language query for metrics with native_sol quote token",
    },
    "metrics_native_sol_direct": {
        "input": {
            "tool": "query_token_metrics",
            "tool_arguments": {
                "token_address": "98mb39tPFKQJ4Bif8iVg9mYb9wsfPZgpgN1sxoVTpump",
                "quote_token": "native_sol",
            },
            "raw_data_only": True,
        },
        "description": "Direct tool call for metrics with native_sol quote token",
    },
    # Test token holders functionality
    "token_holders_natural": {
        "input": {"query": "Show me the top 15 token holders of HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC"},
        "description": "Natural language query for token holders with limit 15",
    },
    "token_holders_direct": {
        "input": {
            "tool": "query_token_holders",
            "tool_arguments": {"token_address": "HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC", "limit": 15},
            "raw_data_only": True,
        },
        "description": "Direct tool call for token holders with limit 15",
    },
    # Test token buyers functionality
    "token_buyers_natural": {
        "input": {"query": "Show me the first 50 buyers of 98mb39tPFKQJ4Bif8iVg9mYb9wsfPZgpgN1sxoVTpump"},
        "description": "Natural language query for first 50 token buyers",
    },
    "token_buyers_direct": {
        "input": {
            "tool": "query_token_buyers",
            "tool_arguments": {"token_address": "98mb39tPFKQJ4Bif8iVg9mYb9wsfPZgpgN1sxoVTpump", "limit": 50},
            "raw_data_only": True,
        },
        "description": "Direct tool call for token buyers with limit 50",
    },
    # Test holder status functionality
    "holder_status_natural": {
        "input": {
            "query": "Check if these addresses ['5ZZnqunFJZr7QgL6ciFGJtbdy35GoVkvv672JTWhVgET', 'DNZwmHYrS7bekmsJeFPxFvkWRfXRPu44phUqZgdK7Pxy', '9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM', '7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU', 'FNNvb1AFDnDVPkocEri8mWbJ1952HQZtFLuwPiUjSJQ'] are still holding 4TBi66vi32S7J8X1A6eWfaLHYmUXu7CStcEmsJQdpump"
        },
        "description": "Natural language query for holder status with multiple test addresses",
    },
    "holder_status_direct": {
        "input": {
            "tool": "query_holder_status",
            "tool_arguments": {
                "token_address": "4TBi66vi32S7J8X1A6eWfaLHYmUXu7CStcEmsJQdpump",
                "buyer_addresses": [
                    "5ZZnqunFJZr7QgL6ciFGJtbdy35GoVkvv672JTWhVgET",
                    "DNZwmHYrS7bekmsJeFPxFvkWRfXRPu44phUqZgdK7Pxy",
                    "9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM",
                    "7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU",
                    "FNNvb1AFDnDVPkocEri8mWbJ1952HQZtFLuwPiUjSJQ",
                ],
            },
            "raw_data_only": True,
        },
        "description": "Direct tool call for holder status with multiple test addresses",
    },
    # Test top traders functionality
    "top_traders_natural": {
        "input": {"query": "List the top 20 traders of 98mb39tPFKQJ4Bif8iVg9mYb9wsfPZgpgN1sxoVTpump by volume"},
        "description": "Natural language query for top 20 traders by volume",
    },
    "top_traders_direct": {
        "input": {
            "tool": "query_top_traders",
            "tool_arguments": {"token_address": "98mb39tPFKQJ4Bif8iVg9mYb9wsfPZgpgN1sxoVTpump", "limit": 20},
            "raw_data_only": True,
        },
        "description": "Direct tool call for top traders with limit 20",
    },
    # Test trending tokens
    "trending_tokens_natural": {
        "input": {"query": "Get top 15 trending tokens on Solana"},
        "description": "Natural language query for top 15 trending tokens",
    },
    "trending_tokens_direct": {
        "input": {"tool": "get_top_trending_tokens", "tool_arguments": {"limit": 15}},
        "description": "Direct tool call for trending tokens with limit 15",
    },
    # Test with raw_data_only flag
    "detailed_analysis_raw": {
        "input": {
            "query": "Get detailed token analysis for HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC",
            "raw_data_only": True,
        },
        "description": "Detailed token analysis with raw_data_only=True",
    },
    # Native SOL specific functionality tests
    "native_sol_metrics": {
        "input": {
            "tool": "query_token_metrics",
            "tool_arguments": {"token_address": "11111111111111111111111111111111", "quote_token": "sol"},
            "raw_data_only": True,
        },
        "description": "Native SOL token metrics test",
    },
    "native_sol_as_quote": {
        "input": {
            "tool": "query_token_metrics",
            "tool_arguments": {
                "token_address": "98mb39tPFKQJ4Bif8iVg9mYb9wsfPZgpgN1sxoVTpump",
                "quote_token": "native_sol",
            },
            "raw_data_only": True,
        },
        "description": "Using native_sol as quote token test",
    },
    "native_sol_holders": {
        "input": {
            "tool": "query_token_holders",
            "tool_arguments": {"token_address": "11111111111111111111111111111111", "limit": 10},
            "raw_data_only": True,
        },
        "description": "Native SOL holders test",
    },
    "native_sol_buyers": {
        "input": {
            "tool": "query_token_buyers",
            "tool_arguments": {"token_address": "11111111111111111111111111111111", "limit": 20},
            "raw_data_only": True,
        },
        "description": "Native SOL buyers test",
    },
    "native_sol_traders": {
        "input": {
            "tool": "query_top_traders",
            "tool_arguments": {"token_address": "11111111111111111111111111111111", "limit": 15},
            "raw_data_only": True,
        },
        "description": "Native SOL top traders test",
    },
    # Price movement analysis
    "price_analysis": {
        "input": {
            "query": "Analyze price movements and trading volume for token 98mb39tPFKQJ4Bif8iVg9mYb9wsfPZgpgN1sxoVTpump in the last hour"
        },
        "description": "Price movements and trading volume analysis",
    },
    # Test with different quote token addresses directly
    "direct_quote_address": {
        "input": {
            "tool": "query_token_metrics",
            "tool_arguments": {
                "token_address": "98mb39tPFKQJ4Bif8iVg9mYb9wsfPZgpgN1sxoVTpump",
                "quote_token": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",  # USDC direct address
            },
            "raw_data_only": True,
        },
        "description": "Direct quote address test with USDC address",
    },
    # Test large batch holder status (chunking functionality)
    "large_batch_chunking": {
        "input": {
            "tool": "query_holder_status",
            "tool_arguments": {
                "token_address": "98mb39tPFKQJ4Bif8iVg9mYb9wsfPZgpgN1sxoVTpump",
                "buyer_addresses": [
                    "5ZZnqunFJZr7QgL6ciFGJtbdy35GoVkvv672JTWhVgET",
                    "DNZwmHYrS7bekmsJeFPxFvkWRfXRPu44phUqZgdK7Pxy",
                    "9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM",
                    "7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU",
                    "FNNvb1AFDnDVPkocEri8mWbJ1952HQZtFLuwPiUjSJQ",
                ]
                * 12,  # 60 addresses to test chunking functionality
            },
            "raw_data_only": True,
        },
        "description": "Large batch holder status (60 addresses) to test chunking functionality",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(BitquerySolanaTokenInfoAgent, TEST_CASES))
