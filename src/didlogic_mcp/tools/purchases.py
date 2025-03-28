from mcp.server.fastmcp import FastMCP, Context
from . import base
from pydantic import Field
from typing import Optional


def register_tools(mcp: FastMCP):
    @mcp.tool(description="List purchased DIDs in DIDLogic")
    async def list_purchases(
        ctx: Context,
        page: Optional[int] = Field(
            description="Page for purchases", default=None
        ),
        per_page: Optional[int] = Field(
            description="Results per page", default=None
        )
    ) -> str:
        params = {}
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page
        response = await base.call_didlogic_api(
            ctx, "GET",
            "/v1/purchases",
            params=params
        )
        return response.json()

    @mcp.tool(description="List Destinations for DID in DIDLogic")
    async def list_destinations(
            ctx: Context,
            number: str | int = Field(description="DID Number")
    ) -> str:
        response = await base.call_didlogic_api(
            ctx,
            "GET",
            f"/v1/purchases/{number}/destinations"
        )
        return response.json()

    @mcp.tool(description="Add Destination for DID in DIDLogic")
    async def add_destination(
        ctx: Context,
        number: str | int = Field(description="DID Number"),
        callhunt: bool = Field(
            description="Is it ring all group number", default=False
        ),
        active: bool = Field(
            description="Is this destination active", default=False
        ),
        transport: int = Field(
            description="Transport for destination", default=1
        ),
        destination: str | int = Field(description="Destination for DID")
    ) -> str:
        data = {
            "destination[callhunt]": int(callhunt),
            "destination[active]": int(active),
            "destination[transport]": transport,
            "destination[destination]": destination
        }
        response = await base.call_didlogic_api(
            ctx, "POST", f"/v1/purchases/{number}/destinations",
            data=data
        )
        return response.json()

    @mcp.tool(description="Delete Destination for DID in DIDLogic")
    async def delete_destination(
        ctx: Context, number: str | int = Field(
            description="DID Number"), id: int = Field(
            description="Destination ID from list_destinations")) -> str:
        await base.call_didlogic_api(
            ctx, "DELETE",
            f"/v1/purchases/{number}/destinations/{id}"
        )
        return "Destination deleted"
