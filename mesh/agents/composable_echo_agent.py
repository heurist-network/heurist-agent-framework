from typing import Any, Dict

from loguru import logger

from mesh.mesh_agent import MeshAgent


class ComposableEchoAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.metadata.update(
            {
                "name": "ComposableEchoAgent",
                "version": "1.0.0",
                "author": "Heurist Team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "An agent that calls EchoAgent and prefixes its response. This agent is for testing only.",
                "inputs": [{"name": "query", "description": "Text to echo back with prefix", "type": "str"}],
                "outputs": [{"name": "response", "description": "Prefixed echo response", "type": "str"}],
                "tags": ["Test"],
            }
        )

    async def handle_message(self, params: Dict[str, Any]) -> Dict[str, Any]:
        query = params.get("query", "")

        # Create task for EchoAgent
        echo_response = await self.mesh_client.create_task(
            agent_id="EchoAgent",
            task_details={"query": query, "origin_task_id": self.task_id},
            api_key=self.heurist_api_key,
        )

        # Get task ID from response
        echo_task_id = echo_response.get("task_id")
        if not echo_task_id:
            logger.error(f"No task_id in response | Task: {self.task_id}")
            raise ValueError("No task_id in EchoAgent response")

        # Wait for EchoAgent result
        echo_result = await self.mesh_client.poll_result(echo_task_id)
        if not echo_result:
            logger.error(f"Echo task failed | Task: {self.task_id} | Echo task: {echo_task_id}")
            raise RuntimeError(f"Failed to get result from EchoAgent task {echo_task_id}")

        # Get the echoed response
        echoed_text = echo_result.get("response", "")

        # Add prefix to the echoed response
        prefixed_response = f"COMPOSABLE: {echoed_text}"

        return {"response": prefixed_response}

    async def cleanup(self):
        logger.debug(f"Cleaning up | Task: {self.task_id}")
        await self.mesh_client.close()
        await super().cleanup()
