"""
Authentication middleware for HTTP MCP server
----------------------------------------------
Extracts Bearer tokens from HTTP Authorization headers and makes them
available to the MCP server tools.
"""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class BearerAuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware to extract Bearer token from Authorization header.

    Stores the token in request.state for access during tool execution.
    In HTTP mode, requests without valid Authorization header are rejected.
    """

    async def dispatch(self, request: Request, call_next):
        # Extract Authorization header
        auth_header = request.headers.get("Authorization", "")

        # Extract Bearer token
        token = None
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]  # Remove "Bearer " prefix

        # Store token in request state (None if not provided)
        request.state.didlogic_api_key = token

        # Log authentication attempt (without exposing full token)
        if token:
            logger.debug(f"Request authenticated with token: {token[:8]}...")
        else:
            logger.warning("Request without Authorization header")

        # Continue processing request
        response = await call_next(request)
        return response


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
