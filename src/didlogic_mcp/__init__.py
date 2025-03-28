"""
Didlogic MCP Server
------------------
An MCP server implementation for the Didlogic API.
"""

from didlogic_mcp.server import mcp


def server():
    mcp.run()


__all__ = ["server", "mcp"]
