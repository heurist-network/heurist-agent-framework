from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from decorators import with_cache, with_retry, monitor_execution
import asyncio

class MeshAgent(ABC):
    """Base class for all mesh agents"""
    
    def __init__(self):
        self.agent_name: str = self.__class__.__name__
        self.metadata: Dict[str, Any] = {
            'version': '1.0.0',
            'author': None,
            'description': None,
            'external_apis': []
        }
        self._api_clients: Dict[str, Any] = {}
    
    @abstractmethod
    async def handle_message(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming message - must be implemented by subclasses"""
        pass
    
    async def cleanup(self):
        """Cleanup API clients"""
        for client in self._api_clients.values():
            await client.close()
        self._api_clients.clear()

    def __del__(self):
        """Destructor to ensure cleanup of resources"""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(self.cleanup())
            else:
                loop.run_until_complete(self.cleanup())
        except Exception:
            pass
