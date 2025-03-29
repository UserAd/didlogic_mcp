from mcp.server.fastmcp import FastMCP, Context
from . import base


def register_tools(mcp: FastMCP):
    # Balance Tools
    @mcp.tool()
    async def get_balance(ctx: Context) -> str:
        """
            Get the current DIDLogic account balance

            Returns a JSON object with balance in USD
            Example output: `{"balance": 35.22}`
        """
        response = await base.call_didlogic_api(ctx, "GET", "/v1/balance")
        return response.text
