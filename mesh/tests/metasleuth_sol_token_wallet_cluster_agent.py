import asyncio
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).parent.parent.parent))
from mesh.metasleuth_sol_token_wallet_cluster_agent import MetaSleuthSolTokenWalletClusterAgent  # noqa: E402

load_dotenv()


async def run_agent():
    agent = MetaSleuthSolTokenWalletClusterAgent()
    try:
        # Example for direct fetch_token_clusters tool
        agent_input_clusters = {
            "tool": "fetch_token_clusters",
            "tool_arguments": {"address": "tQNVaFm2sy81tWdHZ971ztS5FKaShJUKGAzHMcypump", "page": 1, "page_size": 10},
            "raw_data_only": True,
        }
        agent_output_clusters = await agent.handle_message(agent_input_clusters)

        # Example for direct fetch_cluster_details tool
        agent_input_details = {
            "tool": "fetch_cluster_details",
            "tool_arguments": {"cluster_uuid": "13axGrDoFlaj8E0ruhYfi1", "page": 1, "page_size": 10},
            "raw_data_only": True,
        }
        agent_output_details = await agent.handle_message(agent_input_details)

        # Example for natural language query - token analysis
        agent_input_nl_token = {
            "query": "Analyze the wallet clusters of this Solana token: tQNVaFm2sy81tWdHZ971ztS5FKaShJUKGAzHMcypump",
            "raw_data_only": False,
        }
        agent_output_nl_token = await agent.handle_message(agent_input_nl_token)

        # Example for natural language query - cluster details
        agent_input_nl_cluster = {
            "query": "Show me the details of wallet cluster with UUID 0j7eWWwixWixBYPg5oeVX6",
            "raw_data_only": False,
        }
        agent_output_nl_cluster = await agent.handle_message(agent_input_nl_cluster)

        # Example with raw data only
        agent_input_raw = {
            "query": "Get token cluster data for tQNVaFm2sy81tWdHZ971ztS5FKaShJUKGAzHMcypump",
            "raw_data_only": True,
        }
        agent_output_raw = await agent.handle_message(agent_input_raw)

        script_dir = Path(__file__).parent
        current_file = Path(__file__).stem
        base_filename = f"{current_file}_example"
        output_file = script_dir / f"{base_filename}.yaml"

        yaml_content = {
            "direct_token_clusters": {"input": agent_input_clusters, "output": agent_output_clusters},
            "direct_cluster_details": {"input": agent_input_details, "output": agent_output_details},
            "nl_token_analysis": {"input": agent_input_nl_token, "output": agent_output_nl_token},
            "nl_cluster_details": {"input": agent_input_nl_cluster, "output": agent_output_nl_cluster},
            "raw_data_query": {"input": agent_input_raw, "output": agent_output_raw},
        }

        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(yaml_content, f, allow_unicode=True, sort_keys=False)

        print(f"Results saved to {output_file}")

    finally:
        await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(run_agent())
