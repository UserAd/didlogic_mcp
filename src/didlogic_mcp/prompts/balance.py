"""
Balance Prompts for Didlogic MCP Server
These prompts help users check their current balance and understand usage.
"""

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base


def register_prompts(mcp: FastMCP):
    """Register all balance-related prompts with the MCP server"""

    @mcp.prompt()
    def check_balance() -> list[base.Message]:
        """Check the current account balance"""
        return [
            base.UserMessage("Please check my current Didlogic account balance. "),
            base.UserMessage("Format the response clearly and let me know if the balance is low (under $10)."),
            base.UserMessage("Get didlogic balance")]

    return mcp
