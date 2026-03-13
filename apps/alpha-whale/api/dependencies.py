"""FastAPI dependency injection providers."""

from typing import Annotated

from fastapi import Depends, Request
from langgraph.graph.state import CompiledStateGraph
from supabase import AsyncClient

from api.config import APISettings


def get_supabase(request: Request) -> AsyncClient:
    """Retrieve the shared Supabase client from app state."""
    client: AsyncClient = request.app.state.supabase
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
SupabaseDep = Annotated[AsyncClient, Depends(get_supabase)]
GraphDep = Annotated[CompiledStateGraph, Depends(get_graph)]
SettingsDep = Annotated[APISettings, Depends(get_settings)]
