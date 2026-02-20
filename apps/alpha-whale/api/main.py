"""FastAPI application entry point with lifespan management."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.config import APISettings
from py_core import AsyncHTTPClient, get_logger

logger = get_logger("api")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage shared resources across the app lifetime."""
    settings = APISettings()
    client = AsyncHTTPClient(
        base_url=settings.market_data_base_url,
        timeout=15.0,
    )
    async with client:
        app.state.http_client = client
        app.state.settings = settings
        logger.info("api_started", app_name=settings.app_name)
        yield
    logger.info("api_shutdown")


def create_app() -> FastAPI:
    """Application factory."""
    settings = APISettings()
    app = FastAPI(
        title=settings.app_name,
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    from api.routes import router

    app.include_router(router)

    return app


app = create_app()
