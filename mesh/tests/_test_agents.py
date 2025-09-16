"""
Common test utilities for all agent tests.
Handles file saving, result formatting, and test execution.
"""

import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

import yaml


class AgentTestBase:
    """Base class for standardized agent testing."""

    @staticmethod
    async def run_test(agent_class, test_cases: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
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

        try:
            print(f"\n{'=' * 60}")
            print(f"Testing {agent_class.__name__}")
            print(f"{'=' * 60}")

            for test_name, test_data in test_cases.items():
                print(f"\n[{test_name}] {test_data.get('description', 'No description')}")
                print(f"Input: {test_data['input']}")

                try:
                    output = await agent.handle_message(test_data["input"])
                    results[test_name] = {
                        "input": test_data["input"],
                        "output": output,
                        "description": test_data.get("description", ""),
                        "status": "success",
                    }
                    print("✅ Success")
                except Exception as e:
                    results[test_name] = {
                        "input": test_data["input"],
                        "output": None,
                        "error": str(e),
                        "description": test_data.get("description", ""),
                        "status": "failed",
                    }
                    print(f"❌ Failed: {e}")

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
        # If test_filename not provided, try to get it from sys.argv
        if test_filename is None:
            # Get the script name from command line arguments
            script_path = Path(sys.argv[0])
            test_filename = script_path.stem

        # Determine output directory
        if output_dir is None:
            # Use the directory of the running script
            script_path = Path(sys.argv[0])
            output_dir = script_path.parent

        # Create filename
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

        # Save as YAML
        yaml_file = output_dir / f"{base_filename}.yaml"
        with open(yaml_file, "w", encoding="utf-8") as f:
            yaml.dump(final_results, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

        print("\n📁 Results saved to:")
        print(f"  - {yaml_file}")

        # Print summary
        meta = final_results["metadata"]
        print(f"\n📊 Summary: {meta['passed']}/{meta['total_tests']} tests passed")

        return final_results

    @staticmethod
    async def run_agent_tests(
        agent_class, test_cases: Dict[str, Dict[str, Any]], save_output: bool = True, test_filename: str = None
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
        results = await AgentTestBase.run_test(agent_class, test_cases)

        # Save results if requested
        if save_output:
            # If test_filename not provided, extract from sys.argv
            if test_filename is None:
                script_path = Path(sys.argv[0])
                test_filename = script_path.stem

            AgentTestBase.save_results(results, agent_class.__name__, test_filename)

        return results


# Convenience function for running tests
async def test_agent(agent_class, test_cases, test_filename: str = None):
    """Quick function to test an agent with given test cases."""
    return await AgentTestBase.run_agent_tests(agent_class, test_cases, test_filename=test_filename)
