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

    In HTTP mode, extracts Bearer token from request context and adds it
    to the Authorization header for each API call.
    """
    # Use importlib to force loading the server module, not the server() function

    client = ctx.request_context.lifespan_context.client

    print(f"{ctx.request_context.request.state.didlogic_api_key}")

    # In HTTP/SSE mode, get API key from request.state (set by middleware)
    extra_headers = {}
    if True:
        # Debug: Log what we have in context
        request = getattr(ctx.request_context, "request", None)
        logger.debug(f"Request object: {request}")

        if request:
            logger.debug(f"Request has state: {hasattr(request, 'state')}")
            if hasattr(request, 'state'):
                logger.debug(f"State attributes: {dir(request.state)}")
                logger.debug(f"Has didlogic_api_key: {hasattr(request.state, 'didlogic_api_key')}")

                if hasattr(request.state, "didlogic_api_key"):
                    api_key = request.state.didlogic_api_key
                    if api_key:
                        extra_headers["Authorization"] = f"Bearer {api_key}"
                        logger.debug(f"✅ Using API key from request state: {api_key[:8]}...")
                    else:
                        logger.error(f"❌ No API key found in request state for {server_module.TRANSPORT_MODE.upper()} request!")
                        raise httpx.HTTPStatusError(
                            "Missing Authorization header",
                            request=None,
                            response=httpx.Response(401)
                        )
                else:
                    logger.error(f"❌ request.state exists but no didlogic_api_key attribute!")
            else:
                logger.error(f"❌ Request has no state attribute!")
        else:
            logger.error(f"❌ No request object in context for {server_module.TRANSPORT_MODE.upper()} mode!")

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
