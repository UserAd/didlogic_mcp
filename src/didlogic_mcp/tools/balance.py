from mcp.server.fastmcp import FastMCP, Context
from . import base


def register_tools(mcp: FastMCP):
    # Balance Tools
    @mcp.tool(description="get DIDLogic balance")
    async def get_balance(ctx: Context) -> str:
        """Get the current account balance"""
        response = await base.call_didlogic_api(ctx, "GET", "/v1/balance")
        return response.text
