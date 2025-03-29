from mcp.server.fastmcp import FastMCP, Context
from . import base
from typing import Optional
from pydantic import Field


def register_tools(mcp: FastMCP):
    @mcp.tool()
    async def list_sip_accounts(ctx: Context) -> str:
        """
            List all SIP accounts

            Returns a JSON object with all SIP accounts where:
                id: ID of SIP account
                name: SIP account name (login)
                callerid: CallerID associated with this SIP account
                label: label fot this SIP account
                charge: charge for calls on this month
                talk_time: total talk time for this month
                rewrite_enabled: do SIP account have calling number rewriting rule
                rewrite_cond: prefix to be rewrited (ex: 00)
                rewrite_prefix: prefix to what should be rewritten (ex: 44)
                didinfo_enabled: do DIDLogic will attempt send DID number as TO when receiving calls to this account
                ip_restrict: do we need to allowlist IP addresses for this account
                allowed_ips: IP addresses allowed for this SIP account
                call_restrict: flag indicates what SIP account should have maximum call time
                call_limit: maximum call duration in seconds
                channels_restrict: flag indicates what SIP account should have maximum channels limit
                max_channels: maximum sip channels
                cost_limit: flag indicates what SIP account should have maximum call cost
                max_call_cost: maximum call cost for this SIP account
                created_at: date of creation this SIP account

            Example:
            ```
            {
                "sipaccounts": [
                    {
                        "id": 61,
                        "name": "12345",
                        "callerid": "17254999999",
                        "label": "TEST DEVICE",
                        "host": "dynamic",
                        "charge": "0.0",
                        "talk_time": 0,
                        "rewrite_enabled": false,
                        "rewrite_cond": "8",
                        "rewrite_prefix": "7",
                        "didinfo_enabled": false,
                        "ip_restrict": false,
                        "call_restrict": true,
                        "call_limit": 2800,
                        "channels_restrict": false,
                        "max_channels": 1,
                        "cost_limit": false,
                        "max_call_cost": "5.0",
                        "created_at": "2024-06-03 06:06:47 UTC",
                        "allowed_ips": ["1.2.3.4", "3.4.5.6"]
                    }
                ]
            }
            ```
        """
        response = await base.call_didlogic_api(ctx, "GET", "/v1/sipaccounts")
        return response.json()

    @mcp.tool()
    async def get_sip_account(
            ctx: Context, name: str | int = Field(
            description="Name of SIP account")
    ) -> str:
        """
            Get details about SIP account

            Args:
                name: SIP account name

            Returns a JSON object with SIP account details where:
                id: ID of SIP account
                name: SIP account name (login)
                callerid: CallerID associated with this SIP account
                label: label fot this SIP account
                charge: charge for calls on this month
                talk_time: total talk time for this month
                rewrite_enabled: do SIP account have calling number rewriting rule
                rewrite_cond: prefix to be rewrited (ex: 00)
                rewrite_prefix: prefix to what should be rewritten (ex: 44)
                didinfo_enabled: do DIDLogic will attempt send DID number as TO when receiving calls to this account
                ip_restrict: do we need to allowlist IP addresses for this account
                allowed_ips: IP addresses allowed for this SIP account
                call_restrict: flag indicates what SIP account should have maximum call time
                call_limit: maximum call duration in seconds
                channels_restrict: flag indicates what SIP account should have maximum channels limit
                max_channels: maximum sip channels
                cost_limit: flag indicates what SIP account should have maximum call cost
                max_call_cost: maximum call cost for this SIP account
                created_at: date of creation this SIP account

            Example:
            ```
            {
                "sipaccount": {
                    "id": 61,
                    "name": "12345",
                    "callerid": "17254999999",
                    "label": "TEST DEVICE",
                    "host": "dynamic",
                    "charge": "0.0",
                    "talk_time": 0,
                    "rewrite_enabled": false,
                    "rewrite_cond": "8",
                    "rewrite_prefix": "7",
                    "didinfo_enabled": false,
                    "ip_restrict": false,
                    "call_restrict": true,
                    "call_limit": 2800,
                    "channels_restrict": false,
                    "max_channels": 1,
                    "cost_limit": false,
                    "max_call_cost": "5.0",
                    "created_at": "2024-06-03 06:06:47 UTC",
                    "allowed_ips": ["1.2.3.4", "3.4.5.6"]
                }
            }
            ```
        """

        response = await base.call_didlogic_api(
            ctx, "GET", f"/v1/sipaccounts/{name}"
        )
        return response.json()

    @mcp.tool()
    async def create_sip_account(
        ctx: Context,
        password: str = Field(description="Password for new SIP account"),
        callerid: str | int = Field(
            description="Callerid for use with this SIP account", default=""
        ),
        label: str = Field(description="Label for SIP account", default=""),
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
            description="Enable IP restriction for SIP account", default=False
        ),
        call_restrict: Optional[bool] = Field(
            description="Enable call duration limit for SIP account",
            default=False
        ),
        call_limit: Optional[int] = Field(
            description="Maximum call duration for SIP account in seconds",
            default=0
        ),
        channels_restrict: Optional[bool] = Field(
            description="Enable concurrent calls limit", default=False
        ),
        max_channels: Optional[int] = Field(
            description="Count of concurrent calls limit", default=1
        ),
        cost_limit: Optional[bool] = Field(
            description="Enable maximum call cost for SIP account",
            default=False
        ),
        max_call_cost: Optional[float] = Field(
            description="Maximum call cost for SIP account", default=0
        )
    ) -> str:
        """
            Creates a new SIP account

            Args:
                password: Password to be used for this SIP account
                callerid: CallerID associated with this SIP account
                label: label fot this SIP account
                rewrite_enabled: do SIP account have calling number rewriting rule
                rewrite_cond: prefix to be rewrited (ex: 00)
                rewrite_prefix: prefix to what should be rewritten (ex: 44)
                didinfo_enabled: do DIDLogic will attempt send DID number as TO when receiving calls to this account
                ip_restrict: do we need to allowlist IP addresses for this account
                call_restrict: flag indicates what SIP account should have maximum call time
                call_limit: maximum call duration in seconds
                channels_restrict: flag indicates what SIP account should have maximum channels limit
                max_channels: maximum sip channels
                cost_limit: flag indicates what SIP account should have maximum call cost
                max_call_cost: maximum call cost for this SIP account


            Returns a JSON object with SIP account details where:
                id: ID of SIP account
                name: SIP account name (login)
                callerid: CallerID associated with this SIP account
                label: label fot this SIP account
                charge: charge for calls on this month
                talk_time: total talk time for this month
                rewrite_enabled: do SIP account have calling number rewriting rule
                rewrite_cond: prefix to be rewrited (ex: 00)
                rewrite_prefix: prefix to what should be rewritten (ex: 44)
                didinfo_enabled: do DIDLogic will attempt send DID number as TO when receiving calls to this account
                ip_restrict: do we need to allowlist IP addresses for this account
                allowed_ips: IP addresses allowed for this SIP account
                call_restrict: flag indicates what SIP account should have maximum call time
                call_limit: maximum call duration in seconds
                channels_restrict: flag indicates what SIP account should have maximum channels limit
                max_channels: maximum sip channels
                cost_limit: flag indicates what SIP account should have maximum call cost
                max_call_cost: maximum call cost for this SIP account
                created_at: date of creation this SIP account

            Example:
            ```
            {
                "sipaccount": {
                    "id": 61,
                    "name": "12345",
                    "callerid": "17254999999",
                    "label": "TEST DEVICE",
                    "host": "dynamic",
                    "charge": "0.0",
                    "talk_time": 0,
                    "rewrite_enabled": false,
                    "rewrite_cond": "8",
                    "rewrite_prefix": "7",
                    "didinfo_enabled": false,
                    "ip_restrict": false,
                    "call_restrict": true,
                    "call_limit": 2800,
                    "channels_restrict": false,
                    "max_channels": 1,
                    "cost_limit": false,
                    "max_call_cost": "5.0",
                    "created_at": "2024-06-03 06:06:47 UTC",
                    "allowed_ips": ["1.2.3.4", "3.4.5.6"]
                }
            }
            ```
        """

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

    @mcp.tool()
    async def update_sip_account(
        ctx: Context,
        name: str | int = Field(description="SIP Account name"),
        password: Optional[str] = Field(
            description="Password for SIP account", default=None
        ),
        callerid: Optional[str | int] = Field(
            description="Callerid for use with this SIP account", default=None
        ),
        label: Optional[str] = Field(
            description="Label for SIP account", default=None
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
            description="Enable IP restriction for SIP account", default=None
        ),
        call_restrict: Optional[bool] = Field(
            description="Enable call duration limit for SIP account",
            default=None
        ),
        call_limit: Optional[int] = Field(
            description="Maximum call duration for SIP account in seconds",
            default=None
        ),
        channels_restrict: Optional[bool] = Field(
            description="Enable concurrent calls limit", default=None
        ),
        max_channels: Optional[int] = Field(
            description="Count of concurrent calls limit", default=None
        ),
        cost_limit: Optional[bool] = Field(
            description="Enable maximum call cost for SIP account",
            default=None
        ),
        max_call_cost: Optional[float] = Field(
            description="Maximum call cost for SIP account", default=None
        )
    ) -> str:
        """
            Creates a SIP account

            Args:
                name: SIP account name
                password: Password to be used for this SIP account
                callerid: CallerID associated with this SIP account
                label: label fot this SIP account
                rewrite_enabled: do SIP account have calling number rewriting rule
                rewrite_cond: prefix to be rewrited (ex: 00)
                rewrite_prefix: prefix to what should be rewritten (ex: 44)
                didinfo_enabled: do DIDLogic will attempt send DID number as TO when receiving calls to this account
                ip_restrict: do we need to allowlist IP addresses for this account
                call_restrict: flag indicates what SIP account should have maximum call time
                call_limit: maximum call duration in seconds
                channels_restrict: flag indicates what SIP account should have maximum channels limit
                max_channels: maximum sip channels
                cost_limit: flag indicates what SIP account should have maximum call cost
                max_call_cost: maximum call cost for this SIP account


            Returns a JSON object with SIP account details where:
                id: ID of SIP account
                name: SIP account name (login)
                callerid: CallerID associated with this SIP account
                label: label fot this SIP account
                charge: charge for calls on this month
                talk_time: total talk time for this month
                rewrite_enabled: do SIP account have calling number rewriting rule
                rewrite_cond: prefix to be rewrited (ex: 00)
                rewrite_prefix: prefix to what should be rewritten (ex: 44)
                didinfo_enabled: do DIDLogic will attempt send DID number as TO when receiving calls to this account
                ip_restrict: do we need to allowlist IP addresses for this account
                allowed_ips: IP addresses allowed for this SIP account
                call_restrict: flag indicates what SIP account should have maximum call time
                call_limit: maximum call duration in seconds
                channels_restrict: flag indicates what SIP account should have maximum channels limit
                max_channels: maximum sip channels
                cost_limit: flag indicates what SIP account should have maximum call cost
                max_call_cost: maximum call cost for this SIP account
                created_at: date of creation this SIP account

            Example:
            ```
            {
                "sipaccount": {
                    "id": 61,
                    "name": "12345",
                    "callerid": "17254999999",
                    "label": "TEST DEVICE",
                    "host": "dynamic",
                    "charge": "0.0",
                    "talk_time": 0,
                    "rewrite_enabled": false,
                    "rewrite_cond": "8",
                    "rewrite_prefix": "7",
                    "didinfo_enabled": false,
                    "ip_restrict": false,
                    "call_restrict": true,
                    "call_limit": 2800,
                    "channels_restrict": false,
                    "max_channels": 1,
                    "cost_limit": false,
                    "max_call_cost": "5.0",
                    "created_at": "2024-06-03 06:06:47 UTC",
                    "allowed_ips": ["1.2.3.4", "3.4.5.6"]
                }
            }
            ```
        """
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

    @mcp.tool()
    async def delete_sip_account(
            ctx: Context, name: str | int = Field(
            description="Name of SIP account")) -> str:
        """
            Delete a SIP account

            Args:
                name: SIP account name

            Returns a `SIP Account deleted` message on success
        """

        await base.call_didlogic_api(
            ctx, "DELETE", f"/v1/sipaccounts/{name}"
        )

        return "SIP Account deleted"
