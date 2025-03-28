#!/usr/bin/env python3
"""
Didlogic MCP Server
------------------
An MCP server implementation that connects to the Didlogic API and exposes
its functionality through tools and prompts.
"""

import os
import httpx

from contextlib import asynccontextmanager
from dataclasses import dataclass
from mcp.server.fastmcp import FastMCP
import didlogic_mcp.tools as tools
import didlogic_mcp.prompts as prompts

# Configuration
BASE_URL = os.environ.get("DIDLOGIC_API_URL", "https://app.didlogic.com/api")
API_KEY = os.environ.get("DIDLOGIC_API_KEY", "")


@dataclass
class DidlogicContext:
    """Context for Didlogic API client"""
    client: httpx.AsyncClient


@asynccontextmanager
async def didlogic_lifespan(server: FastMCP) -> DidlogicContext:
    """Manage Didlogic API client lifecycle"""
    # Initialize API client

    headers = {
        'User-Agent': 'DidlogicMCP 1.0',
        'Authorization': f"Bearer {API_KEY}"
    }

    async with httpx.AsyncClient(base_url=BASE_URL, headers=headers) as client:
        # Test connection by checking balance
        try:
            response = await client.get("/v1/balance")
            response.raise_for_status()
            print(f"Connected to Didlogic API. Balance: {response.text}")
        except Exception as e:
            print(f"Failed to connect to Didlogic API: {e}")

        yield DidlogicContext(client=client)


# Create MCP Server
mcp = FastMCP(
    "Didlogic API",
    description="MCP Server for Didlogic API integration",
    lifespan=didlogic_lifespan,
    dependencies=["httpx>=0.24.0"]
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
