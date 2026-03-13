"""FastAPI application entry point with lifespan management."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.config import APISettings
from ingestion.supabase_client import create_supabase_client
from py_core import get_logger

logger = get_logger("api")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage shared resources across the app lifetime."""
    settings: APISettings = app.state.settings
    app.state.supabase = await create_supabase_client(
        url=settings.supabase_url,
        key=settings.supabase_key.get_secret_value(),
    )
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
    app.state.settings = settings
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
