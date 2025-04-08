import json
import os
import time
from typing import Dict, Optional

import click
import httpx
from dotenv import load_dotenv
from heurist_mesh_client.client import MeshClient
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

load_dotenv()
MESH_METADATA_URL = "https://mesh.heurist.ai/metadata.json"
TEST_INPUTS_FILE = "test_inputs.json"

DISABLED_AGENTS = {"DeepResearchAgent"}  # slow and times out frequently


def fetch_agents_metadata() -> Dict:
    with httpx.Client() as client:
        response = client.get(MESH_METADATA_URL)
        response.raise_for_status()
        return response.json()


def trim_string(s: str, max_length: int = 300) -> str:
    return s if len(s) <= max_length else s[: max_length - 3] + "..."


def execute_test(
    client: MeshClient,
    agent_id: str,
    tool_name: str,
    inputs: Dict,
    console: Console,
    format_output: callable,
) -> tuple[Optional[str], float, Optional[Dict]]:
    console.print(f"\n[bold blue]Testing {agent_id} - {tool_name}[/bold blue]")
    console.print(f"[dim]Inputs: {format_output(str(inputs))}")

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
            console.print(
                Panel(str(error), title=f"[red]{agent_id} - {tool_name} Error[/red]", border_style="red", expand=False)
            )
            return error, elapsed, None

        console.print(
            Panel(
                format_output(str(result)),
                title=f"[green]{agent_id} - {tool_name} Response ({elapsed:.2f}s)[/green]",
                border_style="green",
                expand=False,
            )
        )
        return None, elapsed, result

    except Exception as e:
        elapsed = time.time() - start_time
        error_str = str(e)
        console.print(
            Panel(
                error_str,
                title=f"[red]{agent_id} - {tool_name} Error ({elapsed:.2f}s)[/red]",
                border_style="red",
                expand=False,
            )
        )
        return error_str, elapsed, None


def test_tool(
    client: MeshClient,
    agent_id: str,
    tool_name: str,
    inputs: Dict,
    console: Console,
    format_output: callable,
    test_results: list,
) -> None:
    error, elapsed, result = execute_test(client, agent_id, tool_name, inputs, console, format_output)
    test_results.append((f"{agent_id} - {tool_name}", error, elapsed, inputs, result))


def display_test_summary(
    results: list[tuple[str, Optional[str], float, Dict, Optional[Dict]]],
    skipped: list[str],
    console: Console,
    json_output: Optional[str] = None,
):
    successes = [(name, duration, inputs, result) for name, error, duration, inputs, result in results if not error]
    failures = [(name, error, duration, inputs, result) for name, error, duration, inputs, result in results if error]

    console.print("\n[bold]Test Run Summary[/bold]")

    console.print("\n[bold green]Successful Tests:[/bold green]")
    for name, duration, _, _ in successes:
        console.print(f"✓ {name} ({duration:.2f}s)")

    if failures:
        console.print("\n[bold red]Failed Tests:[/bold red]")
        for name, error, duration, _, _ in failures:
            console.print(f"✗ {name} ({duration:.2f}s)")
            console.print(f"  Error: {error}")

    if skipped:
        console.print("\n[bold yellow]Skipped Tests:[/bold yellow]")
        for test in skipped:
            console.print(f"⚠ {test}")

    total = len(successes) + len(failures)
    success_rate = (len(successes) / total * 100) if total > 0 else 0
    avg_time = sum(duration for _, duration, _, _ in successes) / len(successes) if successes else 0

    console.print("\n[bold]Statistics:[/bold]")
    console.print(f"Total Tests: {total}")
    console.print(f"Success Rate: {success_rate:.1f}%")
    console.print(f"Average Response Time: {avg_time:.2f}s")
    console.print(f"Skipped Tests: {len(skipped)}")

    if json_output:
        agent_results = {}
        for name, error, duration, inputs, result in results:
            agent_id = name.split(" - ")[0]
            tool_name = name.split(" - ")[1]

            if agent_id not in agent_results:
                agent_results[agent_id] = {"tools": {}}

            agent_results[agent_id]["tools"][tool_name] = {
                "success": not error,
                "duration": duration,
                "error": error,
                "result": result,
            }

        json_data = {
            "summary": {"total": total, "success_rate": success_rate, "avg_time": avg_time, "skipped": len(skipped)},
            "agents": agent_results,
            "skipped": skipped,
        }
        with open(json_output, "w") as f:
            json.dump(json_data, f, indent=2)
        console.print(f"\n[green]Test results written to {json_output}[/green]")


def load_test_inputs() -> Dict:
    if not os.path.exists(TEST_INPUTS_FILE):
        return {}
    with open(TEST_INPUTS_FILE, "r") as f:
        return json.load(f)


def save_test_inputs(data: Dict) -> None:
    with open(TEST_INPUTS_FILE, "w") as f:
        json.dump(data, f, indent=2, sort_keys=True)


def generate_sample_inputs(agent_id: str, tools: set) -> Dict:
    sample_inputs = {}
    for tool in tools:
        sample_inputs[tool] = {}
    return sample_inputs


@click.group()
def cli():
    """Heurist Mesh Agents Testing Suite"""
    pass


@cli.command()
def list_agents():
    """List all available agents and their test status"""
    agents_metadata = fetch_agents_metadata()
    test_inputs = load_test_inputs()

    table = Table(show_header=True)
    table.add_column("Agent Name", style="cyan")
    table.add_column("Tools", style="green")
    table.add_column("Test Data", justify="center")

    orphaned_test_agents = set(test_inputs.keys()) - set(agents_metadata["agents"].keys())
    orphaned_tools = {}
    agents_needing_samples = set()

    for agent_id, agent_data in agents_metadata["agents"].items():
        tools = {tool["function"]["name"] for tool in agent_data.get("tools", [])}
        if not tools:
            continue

        if agent_id in test_inputs:
            test_tools = set(test_inputs[agent_id].keys())
            missing_tools = test_tools - tools
            if missing_tools:
                orphaned_tools[agent_id] = missing_tools
        elif tools:  # agent has tools but no test inputs
            agents_needing_samples.add(agent_id)

    if agents_needing_samples or orphaned_test_agents or orphaned_tools:
        table.add_column("Actions", justify="center")

    for agent_id, agent_data in agents_metadata["agents"].items():
        tools = {tool["function"]["name"] for tool in agent_data.get("tools", [])}

        styled_name = f"[cyan]{agent_id}"
        if agent_id in DISABLED_AGENTS:
            styled_name = f"[dim]{agent_id} [red](disabled)[/]"

        if not tools:
            row = [styled_name, "[dim italic]No tools[/]", "[dim]-[/]"]
            if agents_needing_samples or orphaned_test_agents or orphaned_tools:
                row.append("[dim]-[/]")
            table.add_row(*row)
            continue

        tool_names = []
        has_any_test = False
        tool_test_status = []
        actions = []

        for tool in sorted(tools):
            has_test = agent_id in test_inputs and tool in test_inputs[agent_id]
            if has_test:
                has_any_test = True
                tool_names.append(f"[green]{tool}[/]")
                tool_test_status.append("[green]✓[/]")
            else:
                tool_names.append(f"[dim]{tool}[/]")
                tool_test_status.append("[red]✗[/]")

        if agent_id in agents_needing_samples:
            actions.append("[yellow]Generate Sample[/]")
        else:
            actions.append("[dim]-[/]")

        row = [
            styled_name if has_any_test else f"[dim]{agent_id}[/]",
            "\n".join(tool_names),
            "\n".join(tool_test_status),
        ]
        if agents_needing_samples or orphaned_test_agents or orphaned_tools:
            row.append("\n".join(actions))
        table.add_row(*row)

    if orphaned_test_agents:
        table.add_section()
        for agent_id in sorted(orphaned_test_agents):
            tools = list(test_inputs[agent_id].keys())
            row = [
                f"[yellow]{agent_id} [red](missing agent)[/]",
                "\n".join(f"[yellow]{tool}[/]" for tool in tools),
                "[yellow]![/]",
            ]
            if agents_needing_samples or orphaned_test_agents or orphaned_tools:
                row.append("[red]Remove[/]")
            table.add_row(*row)

    if orphaned_tools:
        table.add_section()
        for agent_id, missing_tools in sorted(orphaned_tools.items()):
            row = [
                f"[yellow]{agent_id} [red](has orphaned tools)[/]",
                "\n".join(f"[yellow]{tool} [red](missing tool)[/]" for tool in sorted(missing_tools)),
                "[yellow]![/]",
            ]
            if agents_needing_samples or orphaned_test_agents or orphaned_tools:
                row.append("[red]Remove[/]")
            table.add_row(*row)

    console = Console()
    console.print(table)

    if agents_needing_samples:
        if click.confirm("\nWould you like to generate sample test inputs for any agents?"):
            for agent_id in sorted(agents_needing_samples):
                if click.confirm(f"Generate sample inputs for {agent_id}?"):
                    tools = {tool["function"]["name"] for tool in agents_metadata["agents"][agent_id].get("tools", [])}
                    test_inputs[agent_id] = generate_sample_inputs(agent_id, tools)
                    save_test_inputs(test_inputs)
                    console.print(f"[green]Generated sample inputs for {agent_id}[/green]")

    if orphaned_test_agents or orphaned_tools:
        if click.confirm("\nWould you like to clean up orphaned entries?"):
            for agent_id in orphaned_test_agents:
                del test_inputs[agent_id]
            for agent_id, missing_tools in orphaned_tools.items():
                for tool in missing_tools:
                    del test_inputs[agent_id][tool]
            save_test_inputs(test_inputs)
            console.print("[green]Cleaned up orphaned entries[/green]")


@cli.command()
@click.argument("agent_tool_pairs", required=False)
@click.option("--include-disabled", is_flag=True, help="Include disabled agents in testing")
@click.option("--no-trim", is_flag=True, help="Disable output trimming")
@click.option("--dev", is_flag=True, help="Use development server")
@click.option(
    "--json",
    is_flag=False,
    flag_value="test_results.json",
    default=None,
    help="Path to save test results as JSON (default: test_results.json when no specific tools are provided)",
)
def test_agent(
    agent_tool_pairs: Optional[str] = None,
    include_disabled: bool = False,
    no_trim: bool = False,
    dev: bool = False,
    json: Optional[str] = None,
):
    """Test specific agent-tool pairs. Format: 'agent1,tool1 agent2,tool2' or just 'agent1' to test all tools"""
    if not os.getenv("HEURIST_API_KEY"):
        click.echo("Error: HEURIST_API_KEY environment variable not set")
        return

    # enable json output by default when no specific tools are provided
    if not agent_tool_pairs and json is None:
        json = "test_results.json"

    try:
        agents_metadata = fetch_agents_metadata()
        test_inputs = load_test_inputs()
        client = MeshClient(base_url="http://localhost:8000" if dev else "https://sequencer-v2.heurist.xyz")
        console = Console()
        test_results = []
        skipped_tests = []

        def format_output(s: str) -> str:
            return s if no_trim else trim_string(s)

        if not agent_tool_pairs:
            console.print("\n[bold yellow]Testing all agents with available test inputs[/bold yellow]")
            for test_agent_id, test_tools in test_inputs.items():
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
                        test_tool(client, test_agent_id, tool_name, inputs, console, format_output, test_results)
        else:
            pairs = [pair.strip() for pair in agent_tool_pairs.split()]
            for pair in pairs:
                agent_id = pair.split(",")[0]
                tool = pair.split(",")[1] if "," in pair else None

                if agent_id not in agents_metadata["agents"]:
                    console.print(f"[red]Error: Agent {agent_id} not found[/red]")
                    continue

                if agent_id in DISABLED_AGENTS and not include_disabled:
                    console.print(f"[yellow]Skipping disabled agent: {agent_id}[/yellow]")
                    skipped_tests.append(f"{agent_id}")
                    continue

                agent_tools = {t["function"]["name"] for t in agents_metadata["agents"][agent_id].get("tools", [])}

                if tool:
                    if tool not in agent_tools:
                        console.print(f"[red]Error: Tool {tool} not found in agent {agent_id}[/red]")
                        continue

                    if agent_id in test_inputs and tool in test_inputs[agent_id]:
                        test_tool(
                            client,
                            agent_id,
                            tool,
                            test_inputs[agent_id][tool],
                            console,
                            format_output,
                            test_results,
                        )
                    else:
                        console.print(f"[yellow]No test inputs defined for {agent_id} - {tool}[/yellow]")
                else:
                    if agent_id in test_inputs:
                        for tool_name, inputs in test_inputs[agent_id].items():
                            if tool_name in agent_tools:
                                test_tool(client, agent_id, tool_name, inputs, console, format_output, test_results)
                    else:
                        console.print(f"[yellow]No test inputs defined for agent {agent_id}[/yellow]")

        if test_results:
            display_test_summary(test_results, skipped_tests, console, json)

    except KeyboardInterrupt:
        console.print("\n[bold red]Testing interrupted by user[/bold red]")
        if test_results:
            display_test_summary(test_results, skipped_tests, console, json)
        raise click.Abort()


if __name__ == "__main__":
    cli()
