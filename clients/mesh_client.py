from typing import Dict, Any
import logging
from .base_client import BaseAPIClient

logger = logging.getLogger(__name__)

class MeshClient(BaseAPIClient):
    """Client for invoking other agents through Protocol V2 Server"""
    
    def __init__(self, base_url: str):
        super().__init__(base_url)

    async def create_task(
        self,
        agent_name: str,
        parameters: Dict[str, Any],
        api_key: str
    ) -> Dict[str, Any]:
        """Create a task for another agent through Protocol V2 Server
        
        Args:
            agent_name: Name of the agent to invoke
            parameters: Parameters to pass to the agent
            api_key: API key for authentication
            
        Returns:
            Dict containing the server response
            
        Raises:
            aiohttp.ClientError: If the request fails
        """
        
        payload = {
            "task_type": agent_name,
            "task_details": {
                "parameters": parameters
            },
            "api_key": api_key
        }

        try:
            response = await self._make_request(
                method="post",
                endpoint="/mesh_task_create",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            return response
            
        except Exception as e:
            logger.error(f"Failed to create task for agent {agent_name}: {e}")
            raise