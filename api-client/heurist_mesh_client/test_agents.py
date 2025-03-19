import os
import time
from typing import Dict, Optional

import click
import httpx
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from test_inputs import TOOL_TEST_INPUTS

from heurist_mesh_client.client import MeshClient

load_dotenv()
MESH_METADATA_URL = "https://mesh.heurist.ai/mesh_agents_metadata.json"

DISABLED_AGENTS = {"DeepResearchAgent"}  # slow and times out frequently


def fetch_agents_metadata() -> Dict:
    with httpx.Client() as client:
        response = client.get(MESH_METADATA_URL)
        response.raise_for_status()
        return response.json()


def trim_string(s: str, max_length: int = 300) -> str:
    return s if len(s) <= max_length else s[: max_length - 3] + "..."


def execute_tool_test(
    client: MeshClient, agent_id: str, tool: str, inputs: Dict, console: Console
) -> tuple[Optional[str], float]:
    console.print(f"\n[bold blue]Testing {agent_id} - {tool}[/bold blue]")
    console.print(f"[dim]Inputs: {trim_string(str(inputs))}")

    start_time = time.time()
    try:
        result = client.sync_request(agent_id=agent_id, tool=tool, tool_arguments=inputs, raw_data_only=True)
        elapsed = time.time() - start_time

        if isinstance(result, dict) and (
            error := result.get("error") or result.get("errorMessage") or result.get("message")
        ):
            console.print(
                Panel(str(error), title=f"[red]{agent_id} - {tool} Error[/red]", border_style="red", expand=False)
            )
            return error, elapsed

        console.print(
            Panel(
                trim_string(str(result)),
                title=f"[green]{agent_id} - {tool} Response ({elapsed:.2f}s)[/green]",
                border_style="green",
                expand=False,
            )
        )
        return None, elapsed

    except Exception as e:
        elapsed = time.time() - start_time
        error_str = str(e)
        console.print(
            Panel(
                error_str,
                title=f"[red]{agent_id} - {tool} Error ({elapsed:.2f}s)[/red]",
                border_style="red",
                expand=False,
            )
        )
        return error_str, elapsed


def display_test_summary(results: list[tuple[str, Optional[str], float]], skipped: list[str], console: Console):
    successes = [(name, duration) for name, error, duration in results if not error]
    failures = [(name, error, duration) for name, error, duration in results if error]

    console.print("\n[bold]Test Run Summary[/bold]")

    console.print("\n[bold green]Successful Tests:[/bold green]")
    for name, duration in successes:
        console.print(f"✓ {name} ({duration:.2f}s)")

    if failures:
        console.print("\n[bold red]Failed Tests:[/bold red]")
        for name, error, duration in failures:
            console.print(f"✗ {name} ({duration:.2f}s)")
            console.print(f"  Error: {error}")

    if skipped:
        console.print("\n[bold yellow]Skipped Tests:[/bold yellow]")
        for test in skipped:
            console.print(f"⚠ {test}")

    total = len(successes) + len(failures)
    success_rate = (len(successes) / total * 100) if total > 0 else 0
    avg_time = sum(duration for _, duration in successes) / len(successes) if successes else 0

    console.print("\n[bold]Statistics:[/bold]")
    console.print(f"Total Tests: {total}")
    console.print(f"Success Rate: {success_rate:.1f}%")
    console.print(f"Average Response Time: {avg_time:.2f}s")
    console.print(f"Skipped Tests: {len(skipped)}")


@click.group()
def cli():
    """Heurist Mesh Agents Testing Suite"""
    pass


@cli.command()
def list_agents():
    """List all available agents and their test status"""
    agents_metadata = fetch_agents_metadata()

    table = Table(show_header=True)
    table.add_column("Agent Name")
    table.add_column("Tools")
    table.add_column("Has Test Data")

    for agent_id, agent_data in agents_metadata["agents"].items():
        tools = [tool["function"]["name"] for tool in agent_data.get("tools", [])]
        table.add_row(agent_id, "\n".join(tools) if tools else "No tools", "✓" if agent_id in TOOL_TEST_INPUTS else "✗")

    Console().print(table)


@cli.command()
@click.argument("agent_tool_pairs", required=False)
@click.option("--include-disabled", is_flag=True, help="Include disabled agents in testing")
def test_agent(agent_tool_pairs: Optional[str] = None, include_disabled: bool = False):
    """Test specific agent-tool pairs. Format: 'agent1,tool1 agent2,tool2'"""
    if not os.getenv("HEURIST_API_KEY"):
        click.echo("Error: HEURIST_API_KEY environment variable not set")
        return

    try:
        agents_metadata = fetch_agents_metadata()
        client = MeshClient()
        console = Console()
        test_results = []
        skipped_tests = []

        if not agent_tool_pairs:
            console.print("\n[bold yellow]Testing all agents with available test inputs[/bold yellow]")
            for test_agent_id, test_tools in TOOL_TEST_INPUTS.items():
                if test_agent_id not in agents_metadata["agents"]:
                    console.print(f"[red]Skipping {test_agent_id} - not found in metadata[/red]")
                    continue

                if test_agent_id in DISABLED_AGENTS and not include_disabled:
                    console.print(f"[yellow]Skipping disabled agent: {test_agent_id}[/yellow]")
                    skipped_tests.extend(f"{test_agent_id} - {t}" for t in test_tools)
                    continue

                agent_tools = {t["function"]["name"] for t in agents_metadata["agents"][test_agent_id].get("tools", [])}
                for tool_name, inputs in test_tools.items():
                    if tool_name in agent_tools:
                        error, elapsed = execute_tool_test(client, test_agent_id, tool_name, inputs, console)
                        test_results.append((f"{test_agent_id} - {tool_name}", error, elapsed))
        else:
            pairs = [pair.strip() for pair in agent_tool_pairs.split()]
            for pair in pairs:
                try:
                    agent_id, tool = pair.split(",")
                    if agent_id not in agents_metadata["agents"]:
                        console.print(f"[red]Error: Agent {agent_id} not found[/red]")
                        continue

                    if agent_id in DISABLED_AGENTS and not include_disabled:
                        console.print(f"[yellow]Skipping disabled agent: {agent_id}[/yellow]")
                        skipped_tests.append(f"{agent_id} - {tool}")
                        continue

                    agent_tools = {t["function"]["name"] for t in agents_metadata["agents"][agent_id].get("tools", [])}
                    if tool not in agent_tools:
                        console.print(f"[red]Error: Tool {tool} not found in agent {agent_id}[/red]")
                        continue

                    if agent_id in TOOL_TEST_INPUTS and tool in TOOL_TEST_INPUTS[agent_id]:
                        error, elapsed = execute_tool_test(
                            client, agent_id, tool, TOOL_TEST_INPUTS[agent_id][tool], console
                        )
                        test_results.append((f"{agent_id} - {tool}", error, elapsed))
                    else:
                        console.print(f"[yellow]No test inputs defined for {agent_id} - {tool}[/yellow]")
                except ValueError:
                    console.print(f"[red]Error: Invalid pair format: {pair}. Use 'agent,tool'[/red]")

        if test_results:
            display_test_summary(test_results, skipped_tests, console)

    except KeyboardInterrupt:
        console.print("\n[bold red]Testing interrupted by user[/bold red]")
        if test_results:
            display_test_summary(test_results, skipped_tests, console)
        raise click.Abort()


if __name__ == "__main__":
    cli()
