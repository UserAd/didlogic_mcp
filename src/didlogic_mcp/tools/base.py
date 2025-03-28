from mcp.server.fastmcp import Context
from typing import Dict, Optional
import httpx


async def call_didlogic_api(
    ctx: Context,
    method: str,
    path: str,
    params: Optional[Dict] = None,
    data: Optional[Dict] = None,
    json: Optional[Dict] = None
) -> httpx.Response:
    """Make a call to the Didlogic API"""
    client = ctx.request_context.lifespan_context.client
    response = await client.request(
        method=method,
        url=path,
        params=params,
        data=data,
        json=json
    )
    response.raise_for_status()
    return response
