from mcp.server.fastmcp import FastMCP, Context
from . import base
from typing import Dict, Optional
from pydantic import Field


def register_tools(mcp: FastMCP):
    @mcp.tool(
        description="list available countries for purchase DID in DIDLogic"
    )
    async def list_countries(
            ctx: Context,
            sms_enabled: Optional[bool] = Field(
                description="Filter sms enabled numbers", default=None
            )
    ) -> Dict:
        params = {}
        if sms_enabled is not None:
            params["sms_enabled"] = int(sms_enabled)
        response = await base.call_didlogic_api(
            ctx,
            "GET",
            "/v2/buy/countries",
            params=params
        )
        return response.json()

    @mcp.tool(description="List country regions")
    async def list_country_regions(
        ctx: Context,
        country_id: int = Field(description="Country ID")
    ) -> Dict:
        response = await base.call_didlogic_api(
            ctx,
            "GET",
            f"/v2/buy/countries/{country_id}/regions"
        )
        return response.json()

    @mcp.tool(description="List country cities")
    async def list_country_cities(
        ctx: Context,
        country_id: int = Field(description="Country ID")
    ) -> Dict:
        response = await base.call_didlogic_api(
            ctx,
            "GET",
            f"/v2/buy/countries/{country_id}/cities"
        )
        return response.json()

    @mcp.tool(description="List country cities in region")
    async def list_country_cities_in_region(
        ctx: Context,
        country_id: int = Field(description="Country ID"),
        region_id: int = Field(description="Region ID")
    ) -> Dict:
        response = await base.call_didlogic_api(
            ctx,
            "GET",
            f"/v2/buy/countries/{country_id}/regions/{region_id}/cities"
        )
        return response.json()

    @mcp.tool(description="List DIDs in country city")
    async def list_dids_in_country_city(
        ctx: Context,
        country_id: int = Field(description="Country ID"),
        city_id: int = Field(description="City ID"),
        page: Optional[int] = Field(description="Search page", default=None),
        per_page: Optional[int] = Field(
            description="Search per page", default=None
        )
    ) -> Dict:
        params = {}
        if page is not None:
            params["page"] = page
        if per_page is not None:
            params["per_page"] = per_page
        response = await base.call_didlogic_api(
            ctx,
            "GET",
            f"/v2/buy/countries/{country_id}/cities/{city_id}/dids",
            params=params
        )
        return response.json()

    @mcp.tool(description="Purchase DID in DIDLogic")
    async def purchase_did(
        ctx: Context,
        number: str | int = Field(
            description="DID number for purchase"
        )
    ) -> Dict:
        response = await base.call_didlogic_api(
            ctx, "POST",
            "/v2/buy/purchase",
            data={"did_numbers": number}
        )
        return response.json()

    @mcp.tool(description="Remove DID from your DIDLogic account")
    async def remove_purchased_did(
        ctx: Context,
        number: str | int = Field(
            description="Number for remove from DIDLogic account"
        )
    ) -> Dict:
        response = await base.call_didlogic_api(
            ctx, "DELETE",
            "/v2/buy/purchase",
            data={"did_numbers": number}
        )
        return response.json()
