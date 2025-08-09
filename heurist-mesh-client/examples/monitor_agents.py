import asyncio
import json
import logging
import os
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import Optional

import click
import httpx
from dotenv import load_dotenv
from heurist_mesh_client.client import MeshClient
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway


# Logger setup
class BracketColorFormatter(logging.Formatter):
    BLUE = "\033[34m"
    GREEN = "\033[32m"
    RED = "\033[31m"
    RESET = "\033[0m"
    WHITE = "\033[37m"

    def format(self, record):
        prefix = getattr(record, "prefix", "")
        level = record.levelname
        prefix_str = f"{self.BLUE}[{prefix}]{self.RESET}" if prefix else ""
        level_str = f"{self.RED}[{level}]{self.RESET}" if level == "ERROR" else f"[{level}]"
        time_str = datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S")
        msg = record.getMessage()
        return f"| {time_str} {prefix_str} {level_str} {msg}"


class PrefixAdapter(logging.LoggerAdapter):
    def __init__(self, logger, prefix):
        super().__init__(logger, {})
        self.prefix = prefix

    def process(self, msg, kwargs):
        kwargs["extra"] = kwargs.get("extra", {})
        kwargs["extra"]["prefix"] = self.prefix
        return msg, kwargs


handler = logging.StreamHandler()
handler.setFormatter(BracketColorFormatter())
base_logger = logging.getLogger("agent_monitor")
base_logger.addHandler(handler)
base_logger.setLevel(logging.INFO)
logger = PrefixAdapter(base_logger, "AGENT")

# Configuration
load_dotenv()
MESH_METADATA_URL = "https://mesh.heurist.ai/metadata.json"
PUSHGATEWAY_URL = os.getenv("PUSHGATEWAY_URL", "151.245.184.3:9091")
JOB_NAME = os.getenv("JOB_NAME", "MESH_AGENTS_DAILY_CHECK")
INTERVAL = 172800  # 48 hours
NUM_WORKERS = 4
TEST_PER_WORKER = 4
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_INPUTS_FILE = os.path.join(SCRIPT_DIR, "test_inputs.json")
DISABLED_AGENTS = {"DeepResearchAgent", "MemoryAgent", "ArbusAgent", "MindAiKolAgent"}
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")


def send_slack_alert(message):
    if not SLACK_WEBHOOK_URL:
        logger.warning("Slack webhook URL not set. Skipping alert.")
        return
    try:
        data = json.dumps({"text": message}).encode("utf-8")
        req = urllib.request.Request(SLACK_WEBHOOK_URL, data=data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req) as response:
            response.read()
        logger.info("Slack alert sent successfully.")
    except Exception as e:
        logger.error(f"Failed to send Slack alert: {e}")


def send_summary_to_slack(stats):
    failing = []
    healthy = []

    for agent_id, agent_data in stats.items():
        total_latency, success_count, total_tests, tool_breakdown = agent_data
        if total_tests == 0:
            continue
        success_rate = (success_count / total_tests) * 100

        if success_rate < 90.0:
            failing.append((agent_id, success_rate, tool_breakdown))
        else:
            healthy.append((agent_id, success_rate))

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

    if failing:
        failing.sort(key=lambda x: x[1])
        failure_text = ""
        for agent, rate, tool_breakdown in failing:
            failure_text += f"• `{agent}` → {rate:.1f}%\n"
            for tool_name, (tool_success, tool_total) in tool_breakdown.items():
                tool_rate = (tool_success / tool_total * 100) if tool_total > 0 else 0
                failure_text += f"  ** {tool_name} = {tool_rate:.0f}%\n"
            failure_text += "\n"

        healthy.sort(key=lambda x: x[1], reverse=True)
        top_healthy = ""
        for agent, rate in healthy[:5]:
            top_healthy += f"• `{agent}` → {rate:.1f}%\n"

        message_text = "*🔴 Agent Performance Alert*\n"
        message_text += f"*Time:* {current_time}\n\n"
        message_text += f"*❌ Below Threshold (90%):*\n{failure_text}"
        if top_healthy:
            message_text += f"*✅ Top 5 Healthy Agents:*\n{top_healthy}\n"
        message_text += f"*Summary:* {len(failing)} failing • {len(healthy)} healthy"

    else:
        total_agents = len(healthy)
        avg_success_rate = sum(rate for _, rate in healthy) / total_agents if total_agents > 0 else 0
        healthy.sort(key=lambda x: x[1], reverse=True)
        top_performers = ""
        for agent, rate in healthy[:8]:
            top_performers += f"• `{agent}` → {rate:.1f}%\n"
        if len(healthy) > 8:
            top_performers += f"• +{len(healthy) - 8} more agents\n"

        message_text = "*🟢 All Systems Healthy*\n"
        message_text += f"*Time:* {current_time}\n\n"
        message_text += "*📊 Performance Summary:*\n"
        message_text += f"• Total Agents: `{total_agents}`\n"
        message_text += f"• Average Success: `{avg_success_rate:.1f}%`\n\n"
        message_text += f"*🎯 Top Performers:*\n{top_performers}"

    try:
        req = urllib.request.Request(
            SLACK_WEBHOOK_URL,
            data=json.dumps({"text": message_text}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req) as response:
            response.read()

        if failing:
            logger.info("Slack alert sent successfully for failing agents.")
        else:
            logger.info("Slack health status sent successfully - all agents healthy.")
    except Exception as e:
        logger.error(f"Failed to send Slack summary alert: {e}")


def is_agent_hidden(agent_data: dict) -> bool:
    return agent_data.get("metadata", {}).get("hidden", False) is True


def fetch_agents_metadata() -> dict:
    try:
        with httpx.Client() as client:
            response = client.get(MESH_METADATA_URL)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.error(f"Error fetching metadata: {e}")
        return {"agents": {}}


def load_test_inputs() -> dict:
    if not os.path.exists(TEST_INPUTS_FILE):
        logger.error(f"Test inputs file not found: {TEST_INPUTS_FILE}")
        return {}
    try:
        with open(TEST_INPUTS_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading test inputs: {e}")
        return {}


def execute_test(
    client: MeshClient, agent_id: str, tool_name: str, inputs: dict
) -> tuple[Optional[str], float, Optional[dict]]:
    start_time = time.time()
    try:
        result = client.sync_request(agent_id=agent_id, tool=tool_name, tool_arguments=inputs, raw_data_only=True)
        elapsed = time.time() - start_time
        error = None
        if isinstance(result, dict):
            if "error" in result:
                error = result["error"]
            elif "errorMessage" in result:
                error = result["errorMessage"]
            elif "message" in result and isinstance(result["message"], str) and "error" in result["message"].lower():
                error = result["message"]
            elif "data" in result and isinstance(result["data"], dict):
                if "error" in result["data"]:
                    error = result["data"]["error"]
                elif "errorMessage" in result["data"]:
                    error = result["data"]["errorMessage"]
                elif "results" in result["data"] and isinstance(result["data"]["results"], dict):
                    results = result["data"]["results"]
                    if "code" in results and results.get("code") != 0:
                        error = f"{results.get('msg', 'Unknown error')} (code: {results['code']})"
                        if "detail" in results:
                            error += f" - {results['detail']}"
            if not error and "response" in result:
                if not result["response"] and isinstance(result.get("data"), dict) and result["data"].get("error"):
                    error = result["data"]["error"]
        if error:
            logger.error(f"Test failed for {agent_id} - {tool_name}: {error}")
        else:
            logger.info(f"Test succeeded for {agent_id} - {tool_name} in {elapsed:.2f}s")
        return error, elapsed, result
    except Exception as e:
        elapsed = time.time() - start_time
        logger.error(f"Exception during test for {agent_id} - {tool_name}: {e}")
        return str(e), elapsed, None


def test_tool(client: MeshClient, agent_id: str, tool_name: str, inputs: dict) -> tuple[float, int, int]:
    total_latency = 0.0
    success_count = 0
    total_tests = TEST_PER_WORKER
    for _ in range(TEST_PER_WORKER):
        error, elapsed, _ = execute_test(client, agent_id, tool_name, inputs)
        total_latency += elapsed
        if not error:
            success_count += 1
    return total_latency, success_count, total_tests


async def push_to_prometheus(stats: dict):
    send_summary_to_slack(stats)
    try:
        registry = CollectorRegistry()
        for agent_id, agent_data in stats.items():
            total_latency, success_count, total_tests, _ = agent_data
            metric_name = agent_id.replace("-", "_").replace(" ", "_")
            avg_latency = total_latency / total_tests if total_tests > 0 else 0.0
            success_rate = (success_count / total_tests * 100) if total_tests > 0 else 0.0
            latency_metric = Gauge(f"{metric_name}_latency", f"Average latency for {agent_id}", registry=registry)
            latency_metric.set(avg_latency if avg_latency else float("nan"))
            success_metric = Gauge(
                f"{metric_name}_success_rate", f"Success rate for {agent_id} (percentage)", registry=registry
            )
            success_metric.set(success_rate)
            logger.info(f"Pushing metrics for {agent_id}: success_rate={success_rate:.2f}%, latency={avg_latency:.2f}s")
        push_to_gateway(PUSHGATEWAY_URL, job=JOB_NAME, registry=registry)
        logger.info(f"Metrics pushed to Prometheus at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    except Exception as e:
        logger.error(f"Error pushing metrics to Prometheus: {e}")
        send_slack_alert(f"Failed to push metrics to Prometheus: {e}")


def run_tests_for_agent(agent_id: str, client: MeshClient, test_inputs: dict, agents_metadata: dict) -> dict:
    stats = {}
    if agent_id not in agents_metadata["agents"]:
        logger.error(f"Agent {agent_id} not found in metadata")
        return stats
    if agent_id in DISABLED_AGENTS:
        logger.info(f"Skipping disabled agent: {agent_id}")
        return stats
    if is_agent_hidden(agents_metadata["agents"][agent_id]):
        logger.info(f"Skipping hidden agent: {agent_id}")
        return stats
    agent_tools = {t["function"]["name"] for t in agents_metadata["agents"][agent_id].get("tools", [])}
    total_latency = 0.0
    total_success_count = 0
    total_tests = 0
    tool_breakdown = {}

    with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
        futures = []
        for tool_name, inputs in test_inputs.get(agent_id, {}).items():
            if tool_name in agent_tools:
                futures.append((tool_name, executor.submit(test_tool, client, agent_id, tool_name, inputs)))
            else:
                logger.warning(f"Tool {tool_name} not found for agent {agent_id}")

        for tool_name, future in futures:
            tool_latency, tool_success_count, tool_total_tests = future.result()
            total_latency += tool_latency
            total_success_count += tool_success_count
            total_tests += tool_total_tests
            tool_breakdown[tool_name] = (tool_success_count, tool_total_tests)

    if total_tests > 0:
        stats[agent_id] = (total_latency, total_success_count, total_tests, tool_breakdown)
    return stats


async def run_all_tests(continuous: bool = False):
    if not os.getenv("HEURIST_API_KEY"):
        logger.error("HEURIST_API_KEY environment variable not set")
        return
    agents_metadata = fetch_agents_metadata()
    test_inputs = load_test_inputs()
    client = MeshClient(base_url="https://sequencer-v2.heurist.xyz", timeout=90)
    while True:
        start_time = time.time()
        logger.info(f"Starting test batch at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        stats = {}
        for agent_id in test_inputs.keys():
            agent_stats = run_tests_for_agent(agent_id, client, test_inputs, agents_metadata)
            stats.update(agent_stats)
        await push_to_prometheus(stats)
        if not continuous:
            break
        sleep_time = max(0, INTERVAL - (time.time() - start_time))
        logger.info(f"Batch completed. Next batch in {sleep_time / 60:.2f} minutes")
        await asyncio.sleep(sleep_time)


async def run_specific_agent(agent_id: str):
    if not os.getenv("HEURIST_API_KEY"):
        logger.error("HEURIST_API_KEY environment variable not set")
        return
    agents_metadata = fetch_agents_metadata()
    if agent_id not in agents_metadata["agents"]:
        logger.error(f"Agent {agent_id} not found")
        return
    test_inputs = load_test_inputs()
    if agent_id not in test_inputs:
        logger.error(f"No test inputs defined for agent {agent_id}")
        return
    client = MeshClient(base_url="https://sequencer-v2.heurist.xyz", timeout=90)
    logger.info(f"Starting test for agent {agent_id}")
    stats = run_tests_for_agent(agent_id, client, test_inputs, agents_metadata)
    await push_to_prometheus(stats)
    logger.info(f"Completed test for agent {agent_id}")


@click.command()
@click.argument("agent_name", required=False)
def main(agent_name: Optional[str] = None):
    """Run agent tests and push metrics to Prometheus. Run without arguments for all agents, or specify an agent name."""
    if agent_name:
        asyncio.run(run_specific_agent(agent_name))
    else:
        asyncio.run(run_all_tests(continuous=True))


if __name__ == "__main__":
    main()
