import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from mesh.agents.layerhop_swap_quote_agent import LayerHopSwapQuoteAgent
from mesh.tests._test_agents import test_agent

TEST_CASES = {
    # Natural language tests
    "bridge_usdc_question": {
        "input": {
            "query": "How much USDC on Arbitrum would I get for 100 USDC on Base?",
            "raw_data_only": False,
        },
        "description": "Cross-chain stablecoin quote from a natural-language question",
    },
    "evm_to_solana_question": {
        "input": {
            "query": "What's the cheapest way to turn 0.05 ETH on Ethereum into SOL on Solana?",
            "raw_data_only": False,
        },
        "description": "EVM to Solana quote (indicative, no wallet given)",
    },
    # Tool call tests
    "quote_base_to_arbitrum": {
        "input": {
            "tool": "get_swap_quote",
            "tool_arguments": {
                "from_chain": "base",
                "from_token": "USDC",
                "amount": "25",
                "to_chain": "arbitrum",
                "to_token": "USDC",
            },
        },
        "description": "Direct tool call: 25 USDC Base -> Arbitrum",
    },
    "quote_with_wallet": {
        "input": {
            "tool": "get_swap_quote",
            "tool_arguments": {
                "from_chain": "ethereum",
                "from_token": "ETH",
                "amount": "0.05",
                "to_chain": "base",
                "to_token": "USDC",
                "sender": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
            },
        },
        "description": "Direct tool call with a sender address: ETH on Ethereum -> USDC on Base",
    },
    "unknown_chain": {
        "input": {
            "tool": "get_swap_quote",
            "tool_arguments": {
                "from_chain": "notachain",
                "from_token": "USDC",
                "amount": "10",
                "to_chain": "base",
                "to_token": "USDC",
            },
        },
        "description": "Error handling: unknown chain slug",
    },
    "list_chains": {
        "input": {"tool": "list_supported_chains", "tool_arguments": {}},
        "description": "Direct tool call: supported chains",
    },
}


if __name__ == "__main__":
    asyncio.run(test_agent(LayerHopSwapQuoteAgent, TEST_CASES))
