import asyncio
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).parent.parent.parent))
from mesh.agents.etherscan_agent import EtherscanAgent  # noqa: E402

load_dotenv()


async def run_agent():
    agent = EtherscanAgent()
    try:
        # Test 1: Natural language query for transaction analysis
        agent_input_tx = {
            "query": "analyze transaction pattern of https://etherscan.io/address/0x2B25B37c683F042E9Ae1877bc59A1Bb642Eb1073",
            "raw_data_only": False,
        }
        agent_output_tx = await agent.handle_message(agent_input_tx)

        # Test 2: Direct tool call for transaction details
        direct_tx_input = {
            "tool": "get_transaction_details",
            "tool_arguments": {
                "chain": "ethereum",
                "txid": "0xd8a484a402a4373221288fed84e9025ed48eba2a45a7294c19289f740ca00fcd",
            },
        }
        direct_tx_output = await agent.handle_message(direct_tx_input)

        # Test 3: Natural language query for address analysis
        agent_input_address = {
            "query": "Get address history for 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045 on ethereum",
            "raw_data_only": False,
        }
        agent_output_address = await agent.handle_message(agent_input_address)

        # Test 4: Direct tool call for address history
        direct_address_input = {
            "tool": "get_address_history",
            "tool_arguments": {"chain": "base", "address": "0x742d35Cc6639C0532fEa3BcdE3524A0be79C3b7B"},
        }
        direct_address_output = await agent.handle_message(direct_address_input)

        # Test 5: Natural language query for token transfers
        agent_input_token_transfers = {
            "query": "Show recent token transfers for 0x55d398326f99059ff775485246999027b3197955 on BSC",
            "raw_data_only": False,
        }
        agent_output_token_transfers = await agent.handle_message(agent_input_token_transfers)

        # Test 6: Direct tool call for ERC20 token transfers
        direct_token_transfers_input = {
            "tool": "get_erc20_token_transfers",
            "tool_arguments": {"chain": "bsc", "address": "0x55d398326f99059ff775485246999027b3197955"},
        }
        direct_token_transfers_output = await agent.handle_message(direct_token_transfers_input)

        # Test 7: Natural language query for token holders
        agent_input_token_holders = {
            "query": "Get top holders for token 0xEF22cb48B8483dF6152e1423b19dF5553BbD818b on Base",
            "raw_data_only": False,
        }
        agent_output_token_holders = await agent.handle_message(agent_input_token_holders)

        # Test 8: Direct tool call for ERC20 top holders
        direct_token_holders_input = {
            "tool": "get_erc20_top_holders",
            "tool_arguments": {"chain": "base", "address": "0xEF22cb48B8483dF6152e1423b19dF5553BbD818b"},
        }
        direct_token_holders_output = await agent.handle_message(direct_token_holders_input)

        # Test 9: Raw data only mode
        raw_data_input = {
            "query": "Analyze transaction 0xabc123 on Arbitrum",
            "raw_data_only": True,
        }
        raw_data_output = await agent.handle_message(raw_data_input)

        # Test 10: Error handling - unsupported chain
        error_input = {
            "tool": "get_transaction_details",
            "tool_arguments": {"chain": "unsupported_chain", "txid": "0x123"},
        }
        error_output = await agent.handle_message(error_input)

        # Test 11: Combined natural language query
        combined_query_input = {
            "query": "Show me both the transfers and top holders for USDT 0x55d398326f99059ff775485246999027b3197955 on BSC",
            "raw_data_only": False,
        }
        combined_query_output = await agent.handle_message(combined_query_input)

        script_dir = Path(__file__).parent
        current_file = Path(__file__).stem
        base_filename = f"{current_file}_example"
        output_file = script_dir / f"{base_filename}.yaml"

        yaml_content = {
            "natural_language_transaction": {"input": agent_input_tx, "output": agent_output_tx},
            "direct_transaction_call": {"input": direct_tx_input, "output": direct_tx_output},
            "natural_language_address": {"input": agent_input_address, "output": agent_output_address},
            "direct_address_call": {"input": direct_address_input, "output": direct_address_output},
            "natural_language_token_transfers": {
                "input": agent_input_token_transfers,
                "output": agent_output_token_transfers,
            },
            "direct_token_transfers_call": {
                "input": direct_token_transfers_input,
                "output": direct_token_transfers_output,
            },
            "natural_language_token_holders": {
                "input": agent_input_token_holders,
                "output": agent_output_token_holders,
            },
            "direct_token_holders_call": {"input": direct_token_holders_input, "output": direct_token_holders_output},
            "raw_data_only": {"input": raw_data_input, "output": raw_data_output},
            "error_handling": {"input": error_input, "output": error_output},
            "combined_query": {"input": combined_query_input, "output": combined_query_output},
        }

        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(yaml_content, f, allow_unicode=True, sort_keys=False)

        print(f"Results saved to {output_file}")

    finally:
        await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(run_agent())
