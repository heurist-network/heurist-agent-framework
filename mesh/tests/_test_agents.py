import asyncio
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

import yaml


class AgentTestBase:
    """Base class for standardized agent testing."""

    @staticmethod
    async def run_test(
        agent_class, test_cases: Dict[str, Dict[str, Any]], delay_seconds: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Execute test cases for an agent and return results.

        Args:
            agent_class: The agent class to instantiate
            test_cases: Dictionary of test_name -> {input, description}

        Returns:
            Dictionary containing all test results
        """
        agent = agent_class()
        results = {}
        last_request_time = 0

        try:
            print(f"\n{'=' * 60}")
            print(f"Testing {agent_class.__name__}")
            if delay_seconds:
                print(f"With {delay_seconds}s delay between requests")
            print(f"{'=' * 60}")

            test_names = list(test_cases.keys())
            for idx, test_name in enumerate(test_names):
                test_data = test_cases[test_name]
                print(f"\n[{test_name}] {test_data.get('description', 'No description')}")
                print(f"Input: {test_data['input']}")

                if delay_seconds and last_request_time > 0:
                    current_time = time.time()
                    time_since_last = current_time - last_request_time
                    if time_since_last < delay_seconds:
                        wait_time = delay_seconds - time_since_last
                        print(f"⏳ Waiting {wait_time:.1f}s before request...")
                        await asyncio.sleep(wait_time)

                try:
                    start_time = time.time()
                    output = await agent.handle_message(test_data["input"])
                    elapsed = time.time() - start_time
                    last_request_time = time.time()
                    results[test_name] = {
                        "input": test_data["input"],
                        "output": output,
                        "description": test_data.get("description", ""),
                        "status": "success",
                        "elapsed_time": elapsed,
                    }
                    print(f"✅ Success ({elapsed:.2f}s)")
                except Exception as e:
                    last_request_time = time.time()
                    results[test_name] = {
                        "input": test_data["input"],
                        "output": None,
                        "error": str(e),
                        "description": test_data.get("description", ""),
                        "status": "failed",
                    }
                    print(f"❌ Failed: {e}")

                if delay_seconds and idx < len(test_names) - 1:
                    print(f"Progress: {idx + 1}/{len(test_names)} completed")

            return results

        finally:
            if hasattr(agent, "cleanup"):
                await agent.cleanup()

    @staticmethod
    def save_results(
        results: Dict[str, Any], agent_name: str, test_filename: str = None, output_dir: Optional[Path] = None
    ):
        """
        Save test results to YAML files.

        Args:
            results: Test results dictionary
            agent_name: Name of the agent being tested (for metadata)
            test_filename: Name to use for the output file (without extension)
            output_dir: Optional output directory (defaults to script directory)
        """
        if test_filename is None:
            script_path = Path(sys.argv[0])
            test_filename = script_path.stem

        if output_dir is None:
            script_path = Path(sys.argv[0])
            output_dir = script_path.parent

        base_filename = f"{test_filename}_example"

        # Add metadata
        final_results = {
            "metadata": {
                "agent": agent_name,
                "test_file": f"{test_filename}.py",
                "timestamp": datetime.now().isoformat(),
                "total_tests": len(results),
                "passed": sum(1 for r in results.values() if r.get("status") == "success"),
                "failed": sum(1 for r in results.values() if r.get("status") == "failed"),
            },
            "results": results,
        }

        yaml_file = output_dir / f"{base_filename}.yaml"
        with open(yaml_file, "w", encoding="utf-8") as f:
            yaml.dump(final_results, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

        print("\n📁 Results saved to:")
        print(f"  - {yaml_file}")

        meta = final_results["metadata"]
        print(f"\n📊 Summary: {meta['passed']}/{meta['total_tests']} tests passed")

        return final_results

    @staticmethod
    async def run_agent_tests(
        agent_class,
        test_cases: Dict[str, Dict[str, Any]],
        save_output: bool = True,
        test_filename: str = None,
        delay_seconds: Optional[float] = None,
    ):
        """
        Main entry point for running agent tests.

        Args:
            agent_class: The agent class to test
            test_cases: Dictionary of test cases
            save_output: Whether to save results to files
            test_filename: Optional filename to use for output (without extension)

        Returns:
            Test results dictionary
        """
        # Run tests
        results = await AgentTestBase.run_test(agent_class, test_cases, delay_seconds)

        if save_output:
            # If test_filename not provided, extract from sys.argv
            if test_filename is None:
                script_path = Path(sys.argv[0])
                test_filename = script_path.stem

            AgentTestBase.save_results(results, agent_class.__name__, test_filename)

        return results


# Convenience function for running tests
async def test_agent(agent_class, test_cases, test_filename: str = None, delay_seconds: Optional[float] = None):
    """Quick function to test an agent with given test cases."""
    return await AgentTestBase.run_agent_tests(
        agent_class, test_cases, test_filename=test_filename, delay_seconds=delay_seconds
    )
