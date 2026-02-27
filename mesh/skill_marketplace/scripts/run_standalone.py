"""Run skill marketplace routes as a standalone server for local testing.

Usage:
    python -m mesh.skill_marketplace.scripts.run_standalone
    # Server starts at http://localhost:8001
    # Docs at http://localhost:8001/docs
"""

import asyncio
import logging
import sys
from contextlib import asynccontextmanager
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

import uvicorn
from fastapi import FastAPI

from mesh.skill_marketplace.db import init_db, close_pool
from mesh.skill_marketplace.routes import router
from mesh.skill_marketplace.admin_routes import admin_router

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s - %(message)s")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_pool()


app = FastAPI(
    title="Heurist Skill Marketplace (standalone)",
    version="0.1.0",
    lifespan=lifespan,
)
app.include_router(router)
app.include_router(admin_router)


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8001)
    parser.add_argument("--reload", action="store_true", default=False)
    args = parser.parse_args()
    if args.reload:
        uvicorn.run(
            "mesh.skill_marketplace.scripts.run_standalone:app",
            host="0.0.0.0", port=args.port, reload=True,
            reload_dirs=[str(Path(__file__).resolve().parent.parent)],
        )
    else:
        uvicorn.run(app, host="0.0.0.0", port=args.port)
