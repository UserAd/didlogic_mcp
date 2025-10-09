"""
Authentication middleware for HTTP MCP server
----------------------------------------------
Extracts Bearer tokens from HTTP Authorization headers and makes them
available to the MCP server tools.
"""

from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.requests import Request
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class BearerAuthMiddleware:
    """
    Middleware to extract Bearer token from Authorization header.

    Stores the token in request.state for access during tool execution.
    Uses pure ASGI interface to be compatible with SSE streaming responses.
    """

    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # Extract Authorization header
        headers = dict(scope.get("headers", []))
        auth_header = headers.get(b"authorization", b"").decode("utf-8")

        # Extract Bearer token
        token = None
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]  # Remove "Bearer " prefix

        # Store token in scope state
        if "state" not in scope:
            scope["state"] = {}
        scope["state"]["didlogic_api_key"] = token

        # Log authentication attempt (without exposing full token)
        if token:
            logger.debug(f"Request authenticated with token: {token[:8]}...")
        else:
            logger.warning("Request without Authorization header")

        # Continue processing request
        await self.app(scope, receive, send)


def get_api_key_from_request(request: Optional[Request]) -> Optional[str]:
    """
    Helper function to extract API key from request state.

    Args:
        request: Starlette Request object (may be None in stdio mode)

    Returns:
        API key string or None if not available
    """
    if request is None:
        return None

    return getattr(request.state, "didlogic_api_key", None)
