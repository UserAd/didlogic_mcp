from mcp.server.fastmcp import FastMCP, Context
from . import base
from typing import Dict
from pydantic import Field


def register_tools(mcp: FastMCP):
    @mcp.tool(description="List DIDLogic SIP account allowed IP list")
    async def get_allowed_ips(
            ctx: Context,
            sipaccount_name: str | int = Field(
                description="Name of sip account"
            )
    ) -> Dict:
        """Get list of allowed IPs for a SIP account"""
        response = await base.call_didlogic_api(
            ctx, "GET",
            f"/v1/sipaccounts/{sipaccount_name}/allowed_ips"
        )
        return response.json()

    @mcp.tool(description="Add IP to allowed list for DIDLogic SIP account")
    async def add_allowed_ip(ctx: Context,
                             sipaccount_name: str | int = Field(
                                 description="Name of sip account"
                             ),
                             ip: str = Field(
                                 description="IP to allow")
                             ) -> Dict:
        """Add an allowed IP to a SIP account"""
        data = {"ip": ip}
        response = await base.call_didlogic_api(
            ctx,
            "POST",
            f"/v1/sipaccounts/{sipaccount_name}/allowed_ips",
            data=data
        )
        return response.json()

    @mcp.tool(
        description="Delete IP from allowed list for DIDLogic SIP account"
    )
    async def delete_allowed_ip(
            ctx: Context,
            sipaccount_name: str | int = Field(
                description="Name of sip account"
            ),
            ip: str = Field(description="IP address")
    ) -> str:
        """Delete an allowed IP from a SIP account"""
        params = {"ip": ip}
        await base.call_didlogic_api(
            ctx,
            "DELETE",
            f"/v1/sipaccounts/{sipaccount_name}/allowed_ips",
            params=params
        )
        return "IP removed successfully"
