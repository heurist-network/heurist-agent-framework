# MeshManager: Task Management and Protocol Communication

## Overview
MeshManager handles communication with the Sequencer V2 Protocol server and manages concurrent task execution. It creates new agent instances on-demand for each incoming task, with built-in concurrency control per agent type.

## Key Components

### Task Flow
1. Manager continuously polls the protocol server for new tasks
2. When a task arrives, if below concurrency limit:
   - Creates new agent instance
   - Executes task asynchronously
   - Returns result to protocol server
3. If at concurrency limit, skip polling for that agent type until capacity frees up

### Concurrency Control
- Each agent type has its own concurrency limit (e.g., `max_concurrency=5`)
- Uses asyncio.Semaphore to naturally limit concurrent tasks
- No explicit scaling needed - tasks are automatically accepted or deferred

## Usage Example
```python
# 1. Register your agent types with concurrency limits
manager.register_agent(DeFiAnalysisAgent, max_concurrency=5)
manager.register_agent(MarketDataAgent, max_concurrency=3)

# 2. Start the manager
await manager.start()

# 3. Monitor status
status = manager.get_status()
# Shows current tasks vs max concurrency per agent type
```