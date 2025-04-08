import asyncio
import logging
import random
from typing import Any, Dict

from mesh.mesh_agent import MeshAgent

logger = logging.getLogger(__name__)


class EchoAgent(MeshAgent):
    def __init__(self):
        super().__init__()
        self.metadata.update(
            {
                "name": "EchoAgent",
                "version": "1.0.0",
                "author": "Heurist Team",
                "author_address": "0x7d9d1821d15B9e0b8Ab98A058361233E255E405D",
                "description": "An agent that simply echoes user input after a random delay (1-4 seconds). This agent is for testing only.",
                "inputs": [{"name": "query", "description": "Any text to echo back.", "type": "str"}],
                "outputs": [{"name": "response", "description": "Echoed text identical to the input.", "type": "str"}],
                "tags": ["Test"],
            }
        )

    async def handle_message(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Sleep for a random 1-4 seconds, then echo the input."""
        query = params.get("query", "")
        # Example of accessing auth info
        user_context = f"heurist_api_key: {self.heurist_api_key}"  # noqa: F841
        delay = random.uniform(1, 4)
        await asyncio.sleep(delay)

        return {"response": query}
