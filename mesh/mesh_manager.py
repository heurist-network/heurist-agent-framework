import asyncio
import aiohttp
import logging
from typing import Dict, Type
import uuid

logger = logging.getLogger(__name__)

class MeshManager:
    """Manages task execution and communication with V2 Protocol server"""
    
    def __init__(self, config: dict):
        self.config = config
        # Mapping of agent_type to {agent_class, semaphore, max_concurrency}
        self.agents: Dict[str, dict] = {}
        self.session: Optional[aiohttp.ClientSession] = None
        self._shutdown = False
        self._poll_task = None
    
    def register_agent(self, agent_class: Type['MeshAgent'], max_concurrency: int = 5):
        """Register an agent type with its concurrency limit"""
        agent_type = agent_class.__name__
        self.agents[agent_type] = {
            'class': agent_class,
            'semaphore': asyncio.Semaphore(max_concurrency),
            'max_concurrency': max_concurrency
        }
        logger.info(f"Registered {agent_type} with max concurrency {max_concurrency}")

    async def start(self):
        """Start the manager and polling loop"""
        self.session = aiohttp.ClientSession()
        self._shutdown = False
        self._poll_task = asyncio.create_task(self._poll_loop())
        logger.info("MeshManager started")
    
    async def stop(self):
        """Stop the manager"""
        self._shutdown = True
        if self._poll_task:
            self._poll_task.cancel()
            try:
                await self._poll_task
            except asyncio.CancelledError:
                pass
        if self.session:
            await self.session.close()
        logger.info("MeshManager stopped")

    async def _poll_loop(self):
        """Main loop for polling tasks from server"""
        while not self._shutdown:
            try:
                for agent_type, info in self.agents.items():
                    # Check if we can handle more tasks for this agent type
                    if info['semaphore'].locked():
                        continue
                    
                    # Poll for new task
                    async with self.session.post(
                        f"{self.config['sequencer_url']}/miner_request",
                        json={
                            "miner_id": str(uuid.uuid4()),
                            "agent_type": agent_type
                        }
                    ) as response:
                        if response.status == 200:
                            task_data = await response.json()
                            if task_data.get('task'):
                                # Spawn new task handler
                                asyncio.create_task(
                                    self._handle_task(agent_type, task_data['task'])
                                )
                
            except Exception as e:
                logger.error(f"Error in polling loop: {e}")
            
            await asyncio.sleep(1)  # Poll frequently but don't overwhelm

    async def _handle_task(self, agent_type: str, task_data: dict):
        """Handle a single task with concurrency control"""
        info = self.agents[agent_type]
        
        async with info['semaphore']:
            try:
                # Create new agent instance for this task
                agent = info['class']()
                
                # Execute task
                result = await agent.handle_message(task_data['params'])
                
                # Submit result
                await self._submit_result(task_data['task_id'], result)
                
            except Exception as e:
                logger.error(f"Error processing task: {e}")
                await self._submit_result(
                    task_data['task_id'],
                    None,
                    error=str(e)
                )

    async def _submit_result(self, task_id: str, result: dict, error: str = None):
        """Submit task result to server"""
        try:
            async with self.session.post(
                f"{self.config['sequencer_url']}/miner_submit",
                json={
                    "task_id": task_id,
                    "result": result,
                    "status": "error" if error else "success",
                    "error": error
                }
            ) as response:
                if response.status != 200:
                    logger.error(f"Failed to submit result: {response.status}")
                    
        except Exception as e:
            logger.error(f"Error submitting result: {e}")
    
    def get_status(self) -> dict:
        """Get current status"""
        return {
            agent_type: {
                'max_concurrency': info['max_concurrency'],
                'current_tasks': info['max_concurrency'] - info['semaphore']._value
            }
            for agent_type, info in self.agents.items()
        }

# Example usage:
async def main():
    # Configuration
    config = {
        'sequencer_url': 'http://localhost:8000'
    }
    
    # Create and start mesh manager
    manager = MeshManager(config)
    
    # Register agents with concurrency limits
    manager.register_agent(DeFiAnalysisAgent, max_concurrency=5)
    manager.register_agent(MarketDataAgent, max_concurrency=3)
    
    # Start manager
    await manager.start()
    
    try:
        # Run indefinitely
        while True:
            # Monitor status periodically
            print(f"Current status: {manager.get_status()}")
            await asyncio.sleep(60)
            
    finally:
        # Clean shutdown
        await manager.stop()

if __name__ == "__main__":
    asyncio.run(main())

# Usage Example
# # Define your agent
# class DeFiAnalysisAgent(MeshAgent):
#     async def handle_message(self, params: dict) -> dict:
#         # Make API calls
#         data = await fetch_defi_data(params)
#         return {'result': data}

# # Start the mesh
# manager = MeshManager({'sequencer_url': 'http://localhost:8000'})
# manager.register_agent(DeFiAnalysisAgent, max_concurrency=5)
# await manager.start()

# # Monitor status
# print(manager.get_status())
# # {'DeFiAnalysisAgent': {'max_concurrency': 5, 'current_tasks': 2}}