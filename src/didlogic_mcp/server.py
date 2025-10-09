#!/usr/bin/env python3
"""
Didlogic MCP Server
------------------
An MCP server implementation that connects to the Didlogic API and exposes
its functionality through tools and prompts.

Supports two modes:
- stdio: Uses DIDLOGIC_API_KEY from environment variable
- HTTP: Extracts Bearer token from Authorization header (no env fallback)
"""

import os
import httpx
import logging

from contextlib import asynccontextmanager
from dataclasses import dataclass
from mcp.server.fastmcp import FastMCP
import didlogic_mcp.tools as tools
import didlogic_mcp.prompts as prompts
from starlette.applications import Starlette
from starlette.routing import Mount
from didlogic_mcp.auth import BearerAuthMiddleware


# Configure logging
logger = logging.getLogger(__name__)

# Configuration
BASE_URL = os.environ.get("DIDLOGIC_API_URL", "https://app.didlogic.com/api")
API_KEY = os.environ.get("DIDLOGIC_API_KEY", "")

# Transport mode - set by __main__.py
TRANSPORT_MODE = "stdio"  # Default mode


@dataclass
class DidlogicContext:
    """Context for Didlogic API client"""
    client: httpx.AsyncClient
    api_key: str  # Store the API key used for this context


def get_api_key_for_request(server: FastMCP) -> str:
    """
    Get API key based on transport mode.

    In stdio mode: Uses environment variable
    In HTTP/SSE mode: Returns empty string (will be set per-request)
    """
    if TRANSPORT_MODE == "stdio":
        if not API_KEY:
            logger.warning("DIDLOGIC_API_KEY not set in environment!")
        return API_KEY
    else:
        # HTTP/SSE mode - API key comes from Authorization header per request
        # The actual key will be injected via middleware
        return ""


@asynccontextmanager
async def didlogic_lifespan(server: FastMCP) -> DidlogicContext:
    """
    Manage Didlogic API client lifecycle.

    Behavior depends on TRANSPORT_MODE:
    - stdio: Uses DIDLOGIC_API_KEY from environment
    - http/sse: Creates client without auth (auth added per-request via middleware)
    """
    api_key = get_api_key_for_request(server)

    headers = {
        'User-Agent': 'DidlogicMCP 1.0',
    }

    # In stdio mode, add Authorization header from environment
    if TRANSPORT_MODE == "stdio" and api_key:
        headers['Authorization'] = f"Bearer {api_key}"
        logger.info("Running server in stdio mode with environment API key")
    else:
        logger.info(f"Running server in {TRANSPORT_MODE} mode")

    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers) as client:
        yield DidlogicContext(client=client, api_key=api_key)


# Create MCP Server with default settings
# Host and port can be reconfigured for HTTP mode
mcp = FastMCP(
    name="Didlogic API",
    instructions="MCP Server for Didlogic API integration",
    lifespan=didlogic_lifespan,
    dependencies=["httpx>=0.24.0"],
    host="127.0.0.1",
    port=8000
)

tools.balance.register_tools(mcp)
tools.sip_accounts.register_tools(mcp)
tools.allowed_ips.register_tools(mcp)
tools.purchases.register_tools(mcp)
tools.purchase.register_tools(mcp)
tools.calls.register_tools(mcp)
tools.transactions.register_tools(mcp)

prompts.balance.register_prompts(mcp)
prompts.sipaccounts.register_prompts(mcp)


def set_transport_mode(mode: str):
    """
    Set the transport mode for the server.

    Must be called before running the server.

    Args:
        mode: "stdio" or "http"
    """
    global TRANSPORT_MODE
    TRANSPORT_MODE = mode
    logger.info(f"Transport mode set to: {mode}")


def configure_http_server(host: str = "127.0.0.1", port: int = 8000):
    """
    Configure host and port for HTTP mode.

    Args:
        host: Host to bind to
        port: Port to bind to
    """
    mcp.settings.host = host
    mcp.settings.port = port
    logger.info(f"HTTP server configured for {host}:{port}")


def create_app_with_middleware(transport: str = "streamable-http"):
    """
    Create a Starlette app with Bearer auth middleware for HTTP/SSE modes.

    Args:
        transport: Transport type ("streamable-http" or "sse")

    Returns:
        Starlette app with middleware
    """
    # Get the appropriate MCP app
    if transport == "sse":
        mcp_app = mcp.sse_app()
    else:
        mcp_app = mcp.streamable_http_app()

    # Wrap with Starlette
    app = Starlette(
        routes=[
            Mount("/", app=mcp_app),
        ],
    )

    # Wrap with Bearer auth middleware (pure ASGI middleware for SSE compatibility)
    app = BearerAuthMiddleware(app)

    logger.info(f"{transport.upper()} app created with Bearer auth middleware")
    return app
