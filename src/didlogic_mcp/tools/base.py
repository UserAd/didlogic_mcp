from mcp.server.fastmcp import Context
from typing import Dict, Optional
import httpx
import logging

logger = logging.getLogger(__name__)


async def call_didlogic_api(
    ctx: Context,
    method: str,
    path: str,
    params: Optional[Dict] = None,
    data: Optional[Dict] = None,
    json: Optional[Dict] = None
) -> httpx.Response:
    """
    Make a call to the Didlogic API.

    In HTTP/SSE mode, extracts Bearer token from request context and adds it
    to the Authorization header for each API call.
    In STDIO mode, uses the API key already configured in the client headers.
    """
    client = ctx.request_context.lifespan_context.client

    # In HTTP/SSE mode, get API key from request.state (set by middleware)
    extra_headers = {}

    # Check if we have a request object (indicates HTTP/SSE mode)
    request = getattr(ctx.request_context, "request", None)

    if request and hasattr(request, 'state') and hasattr(request.state, 'didlogic_api_key'):
        # HTTP/SSE mode: extract API key from request state
        api_key = request.state.didlogic_api_key
        if api_key:
            extra_headers["Authorization"] = f"Bearer {api_key}"
            logger.debug(f"Using API key from request state: {api_key[:8]}...")
        else:
            logger.warning("No API key found in request state")
    else:
        # STDIO mode: API key already in client headers from lifespan
        logger.debug("Using API key from client headers (STDIO mode)")

    response = await client.request(
        method=method,
        url=path,
        params=params,
        data=data,
        json=json,
        headers=extra_headers
    )
    response.raise_for_status()
    return response
