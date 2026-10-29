"""MCP (Model Context Protocol) client support for Shards-ai-agents agents.

This module provides native MCP client functionality, allowing Shards-ai-agents agents
to connect to any MCP-compliant server using various transport types.

Heavy imports (MCPClient, MCPToolResolver, BaseTransport, TransportType) are
lazy-loaded on first access to avoid pulling in the ``mcp`` SDK (~400ms)
when only lightweight config/filter types are needed.
"""

from __future__ import annotations

import importlib
from typing import TYPE_CHECKING, Any

from shards_ai_agents.mcp.config import (
    MCPServerConfig,
    MCPServerHTTP,
    MCPServerSSE,
    MCPServerStdio,
)
from shards_ai_agents.mcp.filters import (
    StaticToolFilter,
    ToolFilter,
    ToolFilterContext,
    create_dynamic_tool_filter,
    create_static_tool_filter,
)


if TYPE_CHECKING:
    from shards_ai_agents.mcp.client import MCPClient
    from shards_ai_agents.mcp.tool_resolver import MCPToolResolver
    from shards_ai_agents.mcp.transports.base import BaseTransport, TransportType

_LAZY: dict[str, tuple[str, str]] = {
    "MCPClient": ("shards_ai_agents.mcp.client", "MCPClient"),
    "MCPToolResolver": ("shards_ai_agents.mcp.tool_resolver", "MCPToolResolver"),
    "BaseTransport": ("shards_ai_agents.mcp.transports.base", "BaseTransport"),
    "TransportType": ("shards_ai_agents.mcp.transports.base", "TransportType"),
}


def __getattr__(name: str) -> Any:
    if name in _LAZY:
        mod_path, attr = _LAZY[name]
        mod = importlib.import_module(mod_path)
        val = getattr(mod, attr)
        globals()[name] = val  # cache for subsequent access
        return val
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "BaseTransport",
    "MCPClient",
    "MCPServerConfig",
    "MCPServerHTTP",
    "MCPServerSSE",
    "MCPServerStdio",
    "MCPToolResolver",
    "StaticToolFilter",
    "ToolFilter",
    "ToolFilterContext",
    "TransportType",
    "create_dynamic_tool_filter",
    "create_static_tool_filter",
]
