import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

import aiohttp
import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

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

app = FastAPI()
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


config = Config()
agents_dict = AgentLoader(config).load_agents()
# passed in at build time, by github actions
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

    agent_cls = agents_dict[request.agent_id]
    agent = agent_cls()

    if request.heurist_api_key:
        agent.set_heurist_api_key(
            request.heurist_api_key
        )  # this is the api key for the agent to authenticate with the heurist api, from config file if not provided

    # Handle API credit deduction if enabled
    credits_api_url = os.getenv("HEURIST_CREDITS_DEDUCTION_API")
    credits_api_auth = os.getenv("HEURIST_CREDITS_DEDUCTION_AUTH")
    if credits_api_url:
        if not credits_api_auth:
            raise HTTPException(status_code=500, detail="Credits API auth not configured")
        try:
            # Parse user_id and api_key, split by first occurrence only, this is passed in from the user
            if "#" in api_key:
                user_id, api_key = api_key.split("#", 1)
            else:
                user_id, api_key = api_key.split("-", 1)

            logger.info(f"Deducting credits for agent {request.agent_id} with user_id {user_id} and api_key {api_key}")
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    credits_api_url,
                    headers={"Authorization": credits_api_auth},
                    json={"user_id": user_id, "api_key": api_key, "model_type": "AGENT", "model_id": request.agent_id},
                ) as response:
                    if response.status != 200:
                        raise HTTPException(status_code=403, detail="API credit validation failed")
        except ValueError:
            raise HTTPException(status_code=401, detail="Invalid API key format")
        except Exception as e:
            logger.error(f"Error validating API credits: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Error validating API credits")

    try:
        result = await agent.call_agent(request.input)
        await agent.cleanup()
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
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")
    uvicorn.run(app, host="0.0.0.0")
