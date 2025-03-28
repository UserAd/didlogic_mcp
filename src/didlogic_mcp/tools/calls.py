from mcp.server.fastmcp import FastMCP, Context
from . import base
from pydantic import Field
from typing import Optional, Literal


def register_tools(mcp: FastMCP):
    @mcp.tool(description="Get call history from didlogic")
    async def get_call_history(
        ctx: Context,
        call_type: Optional[Literal["sip", "incoming"]] = Field(
            description="Type of call, can be sip or incoming", default=None
        ),
        from_date: Optional[str] = Field(
            description="From date in format YYYY-MM-DD", Default=None
        ),
        to_date: Optional[str] = Field(
            description="To date in format YYYY-MM-DD", Default=None
        ),
        number: Optional[str | int] = Field(
            description="Number for search, only digits", default=None
        ),
        sip_account: Optional[str | int] = Field(
            description="SIP Account name for search", default=None
        ),
        from_search: Optional[str | int] = Field(
            description="From number search, only digits", default=None
        ),
        to_search: Optional[str | int] = Field(
            description="To number search, only digits", default=None
        ),
        page: Optional[int] = Field(description="Search page", default=None),
        per_page: Optional[int] = Field(
            description="Search per page", default=None
        )
    ) -> str:
        params = {}
        if call_type is not None:
            params["type"] = call_type
        if from_date is not None:
            params["from"] = from_date
        if to_date is not None:
            params["to"] = to_date
        if number is not None:
            params["filter"] = number
        if sip_account is not None:
            params["sip_account"] = sip_account
        if from_search is not None:
            params["from_search"] = from_search
        if to_search is not None:
            params["to_search"] = to_search
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page

        response = await base.call_didlogic_api(
            ctx, "GET",
            "/v1/calls",
            params=params
        )

        return response.json()
