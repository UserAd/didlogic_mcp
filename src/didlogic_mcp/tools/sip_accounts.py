from mcp.server.fastmcp import FastMCP, Context
from . import base
from typing import Dict, Optional
from pydantic import Field


def register_tools(mcp: FastMCP):
    @mcp.tool(description="list DIDLogic SIP accounts")
    async def list_sip_accounts(ctx: Context) -> Dict:
        """List all SIP accounts"""
        response = await base.call_didlogic_api(ctx, "GET", "/v1/sipaccounts")
        return response.json()

    @mcp.tool(description="Get details about DIDLogic SIP account")
    async def get_sip_account(
            ctx: Context, name: str | int = Field(
            description="Name of sip account")) -> str:
        """Get info about sip account"""
        response = await base.call_didlogic_api(
            ctx, "GET", f"/v1/sipaccounts/{name}"
        )
        return response.json()

    @mcp.tool(description="create DIDLogic SIP account")
    async def create_sip_account(
        ctx: Context,
        password: str = Field(description="Password for new SIP account"),
        callerid: str | int = Field(
            description="Callerid for use with this sip account", default=""
        ),
        label: str = Field(description="Label for sip account", default=""),
        rewrite_enabled: Optional[bool] = Field(
            description="Enable number rewriting for calls", default=False
        ),
        rewrite_cond: Optional[str] = Field(
            description="Prefix to remove from number", default=""
        ),
        rewrite_prefix: Optional[str] = Field(
            description="Prefix to add to number", default=""
        ),
        didinfo_enabled: Optional[bool] = Field(
            description="Enable DID number in inbound calls", default=False
        ),
        ip_restrict: Optional[bool] = Field(
            description="Enable IP restriction for sip account", default=False
        ),
        call_restrict: Optional[bool] = Field(
            description="Enable call duration limit for sip account",
            default=False
        ),
        call_limit: Optional[int] = Field(
            description="Maximum call duration for sip account in seconds",
            default=0
        ),
        channels_restrict: Optional[bool] = Field(
            description="Enable concurrent calls limit", default=False
        ),
        max_channels: Optional[int] = Field(
            description="Count of concurrent calls limit", default=1
        ),
        cost_limit: Optional[bool] = Field(
            description="Enable maximum call cost for sip account",
            default=False
        ),
        max_call_cost: Optional[float] = Field(
            description="Maximum call cost for sip account", default=0
        )
    ) -> Dict:
        """Create a new SIP account"""
        data = {
            "sipaccount[password]": password,
            "sipaccount[callerid]": callerid,
            "sipaccount[label]": label
        }

        # Add optional parameters if provided
        if didinfo_enabled is not None:
            data["sipaccount[didinfo_enabled]"] = didinfo_enabled
        if ip_restrict is not None:
            data["sipaccount[ip_restrict]"] = ip_restrict
        if call_restrict is not None:
            data["sipaccount[call_restrict]"] = call_restrict
        if call_limit is not None:
            data["sipaccount[call_limit]"] = call_limit
        if channels_restrict is not None:
            data["sipaccount[channels_restrict]"] = channels_restrict
        if max_channels is not None:
            data["sipaccount[max_channels]"] = max_channels
        if cost_limit is not None:
            data["sipaccount[cost_limit]"] = cost_limit
        if max_call_cost is not None:
            data["sipaccount[max_call_cost]"] = max_call_cost

        response = await base.call_didlogic_api(
            ctx, "POST", "/v1/sipaccounts", data=data
        )
        return response.json()

    @mcp.tool(description="Update DIDLogic SIP account")
    async def update_sip_account(
        ctx: Context,
        name: str | int = Field(description="SIP Account name"),
        password: Optional[str] = Field(
            description="Password for SIP account", default=None
        ),
        callerid: Optional[str | int] = Field(
            description="Callerid for use with this sip account", default=None
        ),
        label: Optional[str] = Field(
            description="Label for sip account", default=None
        ),
        rewrite_enabled: Optional[bool] = Field(
            description="Enable number rewriting for calls", default=None
        ),
        rewrite_cond: Optional[str] = Field(
            description="Prefix to remove from number", default=None
        ),
        rewrite_prefix: Optional[str] = Field(
            description="Prefix to add to number", default=None
        ),
        didinfo_enabled: Optional[bool] = Field(
            description="Enable DID number in inbound calls", default=None
        ),
        ip_restrict: Optional[bool] = Field(
            description="Enable IP restriction for sip account", default=None
        ),
        call_restrict: Optional[bool] = Field(
            description="Enable call duration limit for sip account",
            default=None
        ),
        call_limit: Optional[int] = Field(
            description="Maximum call duration for sip account in seconds",
            default=None
        ),
        channels_restrict: Optional[bool] = Field(
            description="Enable concurrent calls limit", default=None
        ),
        max_channels: Optional[int] = Field(
            description="Count of concurrent calls limit", default=None
        ),
        cost_limit: Optional[bool] = Field(
            description="Enable maximum call cost for sip account",
            default=None
        ),
        max_call_cost: Optional[float] = Field(
            description="Maximum call cost for sip account", default=None
        )
    ) -> Dict:
        """Update an existing SIP account"""
        data = {}

        # Add all provided parameters
        if password is not None:
            data["sipaccount[password]"] = password
        if callerid is not None:
            data["sipaccount[callerid]"] = callerid
        if label is not None:
            data["sipaccount[label]"] = label
        if rewrite_enabled is not None:
            data["sipaccount[rewrite_enabled]"] = int(rewrite_enabled)
        if rewrite_cond is not None:
            data["sipaccount[rewrite_cond]"] = rewrite_cond
        if rewrite_prefix is not None:
            data["sipaccount[rewrite_prefix]"] = rewrite_prefix
        if didinfo_enabled is not None:
            data["sipaccount[didinfo_enabled]"] = int(didinfo_enabled)
        if ip_restrict is not None:
            data["sipaccount[ip_restrict]"] = int(ip_restrict)
        if call_restrict is not None:
            data["sipaccount[call_restrict]"] = int(call_restrict)
        if call_limit is not None:
            data["sipaccount[call_limit]"] = call_limit
        if channels_restrict is not None:
            data["sipaccount[channels_restrict]"] = int(channels_restrict)
        if max_channels is not None:
            data["sipaccount[max_channels]"] = max_channels
        if cost_limit is not None:
            data["sipaccount[cost_limit]"] = int(cost_limit)
        if max_call_cost is not None:
            data["sipaccount[max_call_cost]"] = max_call_cost

        response = await base.call_didlogic_api(
            ctx, "PUT", f"/v1/sipaccounts/{name}", data=data
        )
        return response.json()

    @mcp.tool(description="Delete DIDLogic SIP account")
    async def delete_sip_account(
            ctx: Context, name: str | int = Field(
            description="Name of sip account")) -> str:
        """Delete a SIP account"""
        await base.call_didlogic_api(
            ctx, "DELETE", f"/v1/sipaccounts/{name}"
        )

        return "SIP Account deleted"
