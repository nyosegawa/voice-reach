"""FastAPI application entry point for VoiceReach backend."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from voicereach.api.health import router as health_router
from voicereach.api.ws import router as ws_router
from voicereach.config import settings
from voicereach.engine.pipeline import Pipeline

logger = logging.getLogger(__name__)

pipeline = Pipeline()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: initialize and shutdown pipeline."""
    logging.basicConfig(
        level=logging.DEBUG if settings.debug else logging.INFO,
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
    )
    await pipeline.initialize()
    logger.info("VoiceReach backend started on %s:%d", settings.host, settings.port)
    yield
    await pipeline.shutdown()
    logger.info("VoiceReach backend stopped")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="VoiceReach",
        version="0.1.0",
        description="AAC communication platform for ALS patients",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_router)
    app.include_router(ws_router)

    return app


app = create_app()


def cli() -> None:
    """CLI entry point for running the server."""
    uvicorn.run(
        "voicereach.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )


if __name__ == "__main__":
    cli()
