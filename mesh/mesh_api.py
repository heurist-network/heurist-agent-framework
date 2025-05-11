import asyncio
import logging
import os
import sys
import time
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

import aiohttp
import uvicorn
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

load_dotenv()
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from mesh.mesh_manager import AgentLoader, Config  # noqa: E402


# exclude `mesh_health` logs as it's used for health checks
class EndpointFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return "GET /mesh_health" not in record.getMessage()


logging.getLogger("uvicorn.access").addFilter(EndpointFilter())
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s - %(message)s")
logger = logging.getLogger("MeshAPI")


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    logger.info("Application shutdown: cleaning up agent pool")
    await agent_pool.cleanup()


app = FastAPI(lifespan=lifespan)
security = HTTPBearer(auto_error=False)

app.add_middleware(
    CORSMiddleware,
    # allow heurist.ai subdomains and localhost for development, mainly for the docs playground
    # ref: http://docs.heurist.ai/dev-guide/heurist-mesh/endpoint
    allow_origin_regex=r"^https?://.*\.heurist\.ai(:\d+)?$|^http?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
    max_age=600,
    allow_credentials=False,
)


class AgentPool:
    """
    Pool of agent instances to be reused across requests.
    This ensures that cached method calls work correctly.
    """

    def __init__(self, agents_dict):
        self.agents_dict = agents_dict
        self.instances = {}  # {agent_id: {"instance": agent_instance, "last_used": timestamp}}
        self.lock = asyncio.Lock()
        self.ttl = 1800  # Time in seconds to keep unused agents

    async def get_agent(self, agent_id):
        """Get an agent instance from the pool or create a new one"""
        async with self.lock:
            now = time.time()

            # Clean up old instances
            to_remove = []
            for id, data in self.instances.items():
                if now - data["last_used"] > self.ttl:
                    to_remove.append(id)
                    # Cleanup the agent
                    try:
                        await data["instance"].cleanup()
                    except Exception as e:
                        logger.warning(f"Error cleaning up agent {id}: {e}")

            for id in to_remove:
                del self.instances[id]

            # Get or create agent instance
            if agent_id not in self.instances:
                if agent_id not in self.agents_dict:
                    raise ValueError(f"Agent {agent_id} not found")

                agent_cls = self.agents_dict[agent_id]
                self.instances[agent_id] = {"instance": agent_cls(), "last_used": now}
                logger.info(f"Created new agent instance: {agent_id}")
            else:
                # Update last used time
                self.instances[agent_id]["last_used"] = now
                logger.info(f"Reusing existing agent instance: {agent_id}")

            return self.instances[agent_id]["instance"]

    async def cleanup(self):
        """Cleanup all agent instances"""
        async with self.lock:
            for id, data in self.instances.items():
                try:
                    await data["instance"].cleanup()
                except Exception as e:
                    logger.warning(f"Error cleaning up agent {id}: {e}")
            self.instances.clear()


config = Config()
agents_dict = AgentLoader(config).load_agents()
agent_pool = AgentPool(agents_dict)
current_commit = os.getenv("GITHUB_SHA", "unknown")


class MeshRequest(BaseModel):
    agent_id: str
    input: Dict[str, Any]
    api_key: str | None = None
    heurist_api_key: str | None = None


async def get_api_key(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security), request: MeshRequest = None
) -> str:
    if credentials:
        return credentials.credentials
    if request and request.api_key:
        return request.api_key
    raise HTTPException(status_code=401, detail="API key is required from either bearer token or request body")


@app.post("/mesh_request")
async def process_mesh_request(request: MeshRequest, api_key: str = Depends(get_api_key)):
    if request.agent_id not in agents_dict:
        raise HTTPException(status_code=404, detail=f"Agent {request.agent_id} not found")

    try:
        # Get agent from pool instead of creating a new instance each time
        agent = await agent_pool.get_agent(request.agent_id)
        origin_api_key = api_key

        if request.heurist_api_key:
            agent.set_heurist_api_key(request.heurist_api_key)  # this is the api key for the agent to use Heurist LLMs

        # Handle API credit deduction if enabled
        credits_api_url = os.getenv("HEURIST_CREDITS_DEDUCTION_API")
        credits_api_auth = os.getenv("HEURIST_CREDITS_DEDUCTION_AUTH")
        if credits_api_url:
            if not credits_api_auth:
                raise HTTPException(status_code=500, detail="Credits API auth not configured")
            try:
                # Parse user_id and api_key, split by first occurrence only, this is passed in from the user
                if "#" in origin_api_key:
                    user_id, api_key = api_key.split("#", 1)
                else:
                    user_id, api_key = api_key.split("-", 1)

                logger.info(
                    f"Deducting credits for agent {request.agent_id} with user_id {user_id} and api_key {api_key}"
                )
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        credits_api_url,
                        headers={"Authorization": credits_api_auth},
                        json={
                            "user_id": user_id,
                            "api_key": api_key,
                            "model_type": "AGENT",
                            "model_id": request.agent_id,
                        },
                    ) as response:
                        if response.status != 200:
                            raise HTTPException(status_code=403, detail="API credit validation failed")
            except ValueError:
                raise HTTPException(status_code=401, detail="Invalid API key format")
            except Exception as e:
                logger.error(f"Error validating API credits: {e}", exc_info=True)
                raise HTTPException(status_code=500, detail="Error validating API credits")

        call_args = dict(request.input)
        call_args["session_context"] = {"api_key": origin_api_key}
        result = await agent.call_agent(call_args)

        # Note: We don't call agent.cleanup() anymore since the agent is reused
        # Agent cleanup is now handled by the pool's TTL mechanism

        return result
    except Exception as e:
        logger.error(f"Error processing request: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/mesh_health")
async def health_check():
    return {
        "status": "ok",
        "commit": current_commit,
        "agents_loaded": len(agents_dict),
        "active_agent_instances": len(agent_pool.instances),
    }


@app.get("/mesh_debug/cache")
async def cache_debug():
    """Debug endpoint to view cache statistics for all agents"""
    stats = {}

    for agent_id, data in agent_pool.instances.items():
        instance = data["instance"]
        agent_stats = {}

        # Get all cache attributes
        for attr_name in dir(instance.__class__):
            if attr_name.startswith("_cache_") and not attr_name.startswith("_cache_ttl_"):
                func_name = attr_name.replace("_cache_", "")
                cache = getattr(instance.__class__, attr_name, {})
                hits = getattr(instance.__class__, f"_cache_hits_{func_name}", 0)
                misses = getattr(instance.__class__, f"_cache_misses_{func_name}", 0)
                ttl_cache = getattr(instance.__class__, f"_cache_ttl_{func_name}", {})

                # Calculate stats
                total_calls = hits + misses
                hit_ratio = (hits / total_calls * 100) if total_calls > 0 else 0

                # Get expiration times for the first few keys
                expirations = {}
                for key in list(cache.keys())[:5]:
                    if key in ttl_cache:
                        expiration = ttl_cache[key]
                        expirations[key] = {
                            "expires_at": expiration.isoformat(),
                            "seconds_left": (expiration - datetime.now()).total_seconds(),
                        }

                agent_stats[func_name] = {
                    "items": len(cache),
                    "hits": hits,
                    "misses": misses,
                    "hit_ratio": f"{hit_ratio:.1f}%",
                    "first_few_keys": list(cache.keys())[:5],
                    "expiration_info": expirations,
                }

        stats[agent_id] = agent_stats

    return {
        "cache_stats": stats,
        "active_agent_instances": len(agent_pool.instances),
        "timestamp": datetime.now().isoformat(),
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")
