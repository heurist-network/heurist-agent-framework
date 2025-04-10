import asyncio
import os
import sys
import time
from importlib import import_module
from pathlib import Path
from pkgutil import iter_modules
from typing import Dict, Type

import aiohttp
from dotenv import load_dotenv
from loguru import logger

project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from mesh.mesh_agent import MeshAgent  # noqa: E402

# Configure loguru
logger.remove()  # Remove default handler
logger.add(
    sys.stderr,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> | <level>{message}</level>",
)


# Configuration
class Config:
    """Configuration management for Mesh Manager"""

    def __init__(self):
        load_dotenv()

        # Server configuration
        self.protocol_v2_url = os.getenv("PROTOCOL_V2_SERVER_URL", "https://sequencer-v2.heurist.xyz")
        self.poll_interval = float(os.getenv("POLL_INTERVAL_SECONDS", "2.0"))
        self.auth_token = os.getenv("PROTOCOL_V2_AUTH_TOKEN", "test_key")
        self.agent_type = "AGENT"


class AgentLoader:
    """Handles dynamic loading of agent modules"""

    def __init__(self, config: Config):
        self.config = config

    def load_agents(self) -> Dict[str, Type[MeshAgent]]:
        agents_dict = {}
        package_name = "mesh.agents"
        found_agents = []
        import_errors = []

        try:
            package = import_module(package_name)
            package_path = Path(package.__file__).parent

            for _, module_name, is_pkg in iter_modules([str(package_path)]):
                if is_pkg:
                    continue

                full_module_name = f"{package_name}.{module_name}"
                try:
                    mod = import_module(full_module_name)
                    for attr_name in dir(mod):
                        attr = getattr(mod, attr_name)
                        if isinstance(attr, type) and issubclass(attr, MeshAgent) and attr is not MeshAgent:
                            agents_dict[attr.__name__] = attr
                            found_agents.append(f"{attr.__name__} ({module_name})")

                except ImportError as e:
                    import_errors.append(f"{module_name}: {str(e)}")
                    continue
                except Exception as e:
                    import_errors.append(f"{module_name}: Unexpected error: {str(e)}")
                    continue

            # Log consolidated messages
            if found_agents:
                logger.info(f"Found agents: {', '.join(found_agents)}")
            if import_errors:
                logger.warning(f"Import errors: {', '.join(import_errors)}")

            return agents_dict

        except Exception as e:
            logger.exception(f"Critical error loading agents: {str(e)}")
            return {}


class MeshManager:
    """
    The MeshManager coordinates tasks between the Protocol V2 server
    and the various MeshAgent implementations. Each agent has its own poll loop.
    """

    def __init__(self, config: Config):
        self.config = config
        self.session: aiohttp.ClientSession = None
        self.agent_loader = AgentLoader(config)
        self.agents_dict = self.agent_loader.load_agents()
        self.active_tasks = {}
        self.tasks = {}  # Tracking poll tasks

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        for task in self.tasks.values():
            task.cancel()
        try:
            await asyncio.gather(*self.tasks.values(), return_exceptions=True)
        except Exception:
            pass
        if self.session:
            await self.session.close()
            self.session = None

    async def poll_server(self, agent_id: str) -> Dict:
        """Handle polling the server for new tasks"""
        headers = {"Authorization": self.config.auth_token, "Content-Type": "application/json"}
        payload = {
            "agent_info": [
                {
                    "agent_id": agent_id,
                    "agent_type": self.config.agent_type,
                }
            ]
        }

        try:
            async with self.session.post(
                f"{self.config.protocol_v2_url}/mesh_manager_poll", json=payload, headers=headers
            ) as resp:
                resp_data = await resp.json()
                return resp_data
        except Exception as e:
            logger.error(f"Poll error | Agent: {agent_id} | Error: {str(e)}")
            return {}

    async def process_task(self, agent_id: str, agent_cls: Type[MeshAgent], task_data: Dict) -> Dict:
        """Handle individual task processing logic"""
        task_id = task_data.get("task_id")
        agent_input = task_data["input"]

        # Handle task origin tracking
        parent_task_id = task_data.get("origin_task_id", task_id)
        if "origin_task_id" not in agent_input:
            agent_input["origin_task_id"] = parent_task_id

        agent = agent_cls()
        if "heurist_api_key" in task_data:
            agent.set_heurist_api_key(task_data["heurist_api_key"])

        inference_start = time.time()
        try:
            result = await agent.call_agent(agent_input)
            inference_latency = time.time() - inference_start
            return {"results": {"success": "true", **result}, "inference_latency": round(inference_latency, 3)}
        except Exception as e:
            logger.error(f"[{agent_id}] Error in handle_message: {e}", exc_info=True)
            return {"results": {"success": "false", "error": str(e)}, "inference_latency": 0}
        finally:
            await agent.cleanup()

    async def submit_result(self, agent_id: str, task_id: str, result: Dict) -> Dict:
        """Handle submitting results back to the server"""
        headers = {"Authorization": self.config.auth_token, "Content-Type": "application/json"}
        submit_data = {
            "task_id": task_id,
            "agent_id": agent_id,
            "agent_type": self.config.agent_type,
            "results": result["results"],
            "inference_latency": result["inference_latency"],
        }

        try:
            async with self.session.post(
                f"{self.config.protocol_v2_url}/mesh_manager_submit", json=submit_data, headers=headers
            ) as resp:
                submit_resp_data = await resp.json()
                logger.info(f"Result submitted | Agent: {agent_id} | Task: {task_id} | Result: {submit_data}")
                return submit_resp_data
        except Exception as e:
            logger.error(f"Result submission failed | Agent: {agent_id} | Task: {task_id} | Error: {str(e)}")
            raise

    async def run_agent_task_loop(self, agent_id: str, agent_cls: Type[MeshAgent]):
        """Main task loop for each agent - polls for tasks and processes them"""
        self.active_tasks[agent_id] = set()

        while True:
            try:
                # Just poll with timeout
                poll_task = asyncio.create_task(self.poll_server(agent_id))
                try:
                    resp_data = await asyncio.wait_for(poll_task, timeout=self.config.poll_interval)

                    if resp_data and "input" in resp_data:
                        task_id = resp_data.get("task_id")
                        self.active_tasks[agent_id].add(task_id)

                        try:
                            logger.info(f"Task started | Agent: {agent_id} | Task: {task_id}")
                            result = await self.process_task(agent_id, agent_cls, resp_data)
                            await self.submit_result(agent_id, task_id, result)
                            logger.info(f"Task completed | Agent: {agent_id} | Task: {task_id}")
                        finally:
                            self.active_tasks[agent_id].remove(task_id)

                except asyncio.TimeoutError:
                    pass  # No task found within timeout

            except Exception as e:
                logger.error(f"Task loop error | Agent: {agent_id} | Error: {str(e)}")

    async def run_forever(self):
        """Creates a polling task for each known agent ID and runs them in parallel."""
        if not self.agents_dict:
            logger.warning("No agents found to run.")
            return

        # Create tasks for each agent
        self.tasks = {}  # Reset tasks dict
        agent_ids = list(self.agents_dict.keys())

        for agent_id, agent_cls in self.agents_dict.items():
            task = asyncio.create_task(self.run_agent_task_loop(agent_id, agent_cls))
            self.tasks[agent_id] = task

        logger.info(f"Started task loops for agents: {', '.join(agent_ids)}")

        try:
            await asyncio.gather(*self.tasks.values())
        except Exception as e:
            logger.error(f"Fatal error in run_forever: {e}", exc_info=True)
            # Cancel all tasks on fatal error
            for task in self.tasks.values():
                task.cancel()
            raise


async def main():
    config = Config()
    async with MeshManager(config) as manager:
        await manager.run_forever()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("MeshManager stopped by user.")
