from mcp.server.fastmcp import FastMCP, Context
from . import base
from typing import Dict
from pydantic import Field


def register_tools(mcp: FastMCP):
    @mcp.tool()
    async def get_allowed_ips(
            ctx: Context,
            sipaccount_name: str | int = Field()
    ) -> Dict:
        """
            Get list of whitelisted IPs for a SIP account

            Args:
                sipaccount_name: Name of SIP account

            Returns a JSON object with array of whitelisted IP for SIP Account
            Example output: { "allowed_ips": [ "88.99.12.33" ] }
        """
        response = await base.call_didlogic_api(
            ctx, "GET",
            f"/v1/sipaccounts/{sipaccount_name}/allowed_ips"
        )
        return response.json()

    @mcp.tool()
    async def add_allowed_ip(ctx: Context,
                             sipaccount_name: str | int = Field(
                                 description="Name of sip account"
                             ),
                             ip: str = Field(
                                 description="IP address to allow")
                             ) -> Dict:
        """
            Whitelist an IP to a SIP account

            Args:
                sipaccount_name: Name of SIP account
                ip: IP address to allow

            Returns a JSON object with all whitelisted IP addresses for account
            Example output: { "allowed_ips": [ "88.99.12.33", "99.33.55.11" ] }

        """
        data = {"ip": ip}
        response = await base.call_didlogic_api(
            ctx,
            "POST",
            f"/v1/sipaccounts/{sipaccount_name}/allowed_ips",
            data=data
        )
        return response.json()

    @mcp.tool()
    async def delete_allowed_ip(
            ctx: Context,
            sipaccount_name: str | int = Field(
                description="Name of sip account"
            ),
            ip: str = Field(description="IP address to remove from whitelist")
    ) -> str:
        """
            Delete an whitelisted IP from a SIP account

            Args:
                sipaccount_name: Name of SIP account
                ip: IP address to remove from whitelist

            Returns "IP removed successfully" when IP removed from whitelisted
        """
        params = {"ip": ip}
        await base.call_didlogic_api(
            ctx,
            "DELETE",
            f"/v1/sipaccounts/{sipaccount_name}/allowed_ips",
            params=params
        )
        return "IP removed successfully"
