"""FastAPI dependency injection providers."""

from typing import Annotated

from fastapi import Depends, Request
from langgraph.graph.state import CompiledStateGraph

from api.config import APISettings
from py_core import AsyncHTTPClient


def get_http_client(request: Request) -> AsyncHTTPClient:
    """Retrieve the shared AsyncHTTPClient from app state."""
    client: AsyncHTTPClient = request.app.state.http_client
    return client


def get_settings(request: Request) -> APISettings:
    """Retrieve shared settings from app state."""
    settings: APISettings = request.app.state.settings
    return settings


def get_graph() -> CompiledStateGraph:
    """Return the compiled LangGraph agent."""
    from agent.graph import app as agent_app

    graph: CompiledStateGraph = agent_app
    return graph


# Type aliases for cleaner route signatures
HTTPClientDep = Annotated[AsyncHTTPClient, Depends(get_http_client)]
GraphDep = Annotated[CompiledStateGraph, Depends(get_graph)]
SettingsDep = Annotated[APISettings, Depends(get_settings)]
